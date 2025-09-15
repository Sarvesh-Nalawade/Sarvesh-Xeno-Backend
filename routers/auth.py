import resend
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from database import models
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.query import validate_user, get_user


email_otp_dict = {}

resend.api_key = os.getenv("RESEND_API_KEY")


router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"message": "unauthorized access"}}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

# PYDANTIC MODE

class UserCredentials(BaseModel):
    email: str 
    otp : int

class VerifyCrendentials(BaseModel):
    email: str

# class UserResponse(BaseModel):
#     email: str
#     username: str


class Token(BaseModel):
    access_token: str
    token_type: str


def send_mail(user_email: str):
    otp = 73462
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [user_email],
        "subject": "Hello World", 
        # send otp in html 
        "html": f"<strong>hi, your otp is: {otp}</strong>"
    }
    email: resend.Email = resend.Emails.send(params)
    
    email_otp_dict[user_email] = otp
    
    return email



def verify_otp(user_email: str, otp: int) -> bool:
    if user_email in email_otp_dict and email_otp_dict[user_email] == otp:
        return True
    return False    


def authenticate_user(request: Request,  db: Session):
    print("request:", request.cookies)
    token = request.cookies.get("access_token")
    # print("token:", token)
    if not token:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not validate credentials")
    payload = jwt.decode(str(token), str(SECRET_KEY), ALGORITHM)
    user_id = payload.get("user_id")
    user = get_user(user_id, db)
    return user
   

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(
    user_id: str,  expires_delta: timedelta
):
    to_encode = {"user_id": user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = str(int(expire.timestamp()))
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    
    return encoded_jwt

    

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(user_credentials: UserCredentials, db: Session = Depends(get_db)): 
    is_verified = verify_otp(user_credentials.email, user_credentials.otp)
    
    if is_verified:
        # TODO: do we need the db in this file
        user = validate_user(user_credentials.email, db)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=360)
        access_token = create_access_token(user.id, access_token_expires)
        
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="access_token", value=access_token, httponly=True, path="/", secure=True, samesite='none')
        # response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")
        
        return response  
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")
    


@router.post("/send-email", status_code=status.HTTP_200_OK)
async def send_email(verify_credentials: VerifyCrendentials):
    send_mail(verify_credentials.email)  


@router.post("/logout")
async def logoutUser():
    try:
        msg = {"message": "Logout successful. We hope to see you again soon!"}
        response = JSONResponse(content=msg)
        response.delete_cookie(key="access_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not logout user.")