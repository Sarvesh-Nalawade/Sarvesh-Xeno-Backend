from database import Session, Select
from database.models import TenantUser 

def validate_user(email_id: str, db : Session):
    stmt = Select(TenantUser).where(TenantUser.email == email_id)
    result = db.execute(stmt).scalar_one_or_none()
    return result

def get_user(user_id : int, db : Session):
    stmt = Select(TenantUser).where(TenantUser.id == user_id)   
    result = db.execute(stmt).scalar_one_or_none()
    return result 
