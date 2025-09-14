from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse  
from routers.auth import authenticate_user
from sqlalchemy.orm import Session
from sqlalchemy import Select
from pydantic import BaseModel
from database import get_db, models


router = APIRouter(
    prefix="/user",
    tags=["files"],
)


mail_default = "sarvesh.vitchennai@gmail.com"

class CustomerModel(BaseModel): 
    id : int 
    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    revenue_generated: float = 100.0
    tags: str | None = None
    
@router.get("/get-customers", response_model=list[CustomerModel], status_code=status.HTTP_200_OK)
async def get_customers(request: Request, db: Session = Depends(get_db)): 

    # user = authen    dfklafkdlsfja;ldskfja;skjflsadklfticate_user(request, db) 
    
    
    shop_id = Select(models.TenantUser.shop_id).where(models.TenantUser.email == mail_default) 
    
    stmt = Select(models.Customer).where(models.Customer.shop_id == shop_id)
    
    results = db.execute(stmt).scalars().all() 

    return results
    
      
    

class VariantModel(BaseModel):  
    title: str
    price: float 
    inv_item_qty : int
    weight : int | None = None
    
@router.get("/get-products", response_model=list[VariantModel], status_code=status.HTTP_200_OK)
async def get_products(request: Request, db: Session = Depends(get_db)): 

    # user = authen    dfklafkdlsfja;ldskfja;skjflsadklfticate_user(request, db) 
    
    
    shop_id = Select(models.TenantUser.shop_id).where(models.TenantUser.email == mail_default) 
    
    stmt = Select(models.Variant).where(models.Variant.shop_id == shop_id)
    
    results = db.execute(stmt).scalars().all() 


    return results



    
      
class OwnerModel(BaseModel):  
    owner: str
    name: str
    
@router.get("/get-shop-details", response_model=list[OwnerModel], status_code=status.HTTP_200_OK)
async def get_shop_details(request: Request, db: Session = Depends(get_db)): 

    # user = authen    dfklafkdlsfja;ldskfja;skjflsadklfticate_user(request, db) 
    
    
    shop_id = Select(models.TenantUser.shop_id).where(models.TenantUser.email == mail_default) 
    
    stmt = Select(models.Shop).where(models.Shop.id == shop_id)
    
    results = db.execute(stmt).scalars().all()

    return results