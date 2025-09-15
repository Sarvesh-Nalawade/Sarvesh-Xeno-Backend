from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from routers.auth import authenticate_user
from sqlalchemy.orm import Session
from sqlalchemy import Select, func
from pydantic import BaseModel
from database import get_db, models
from datetime import datetime


router = APIRouter(
    prefix="/user",
    tags=["files"],
)


mail_default = "sarvesh.vitchennai@gmail.com"


class CustomerModel(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    revenue_generated: float = 100.0
    tags: str | None = None


@router.get(
    "/get-customers", response_model=list[CustomerModel], status_code=status.HTTP_200_OK
)
async def get_customers(request: Request, db: Session = Depends(get_db)):
    # Get shop_id for the default email
    shop_id_subq = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    # Compose query: customers with their total revenue
    stmt = (
        Select(
            models.Customer.id,
            models.Customer.first_name,
            models.Customer.last_name,
            models.Customer.email,
            models.Customer.phone,
            models.Customer.tags,
            func.coalesce(func.sum(models.Order.total_price), 0.0).label(
                "revenue_generated"
            ),
        )
        .outerjoin(models.Order, models.Customer.id == models.Order.customer_id)
        .where(models.Customer.shop_id == shop_id_subq)
        .group_by(
            models.Customer.id,
            models.Customer.first_name,
            models.Customer.last_name,
            models.Customer.email,
            models.Customer.phone,
            models.Customer.tags,
        )
    )

    results = db.execute(stmt).all()
    # Map results to CustomerModel
    customers = [
        CustomerModel(
            id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            email=row.email,
            phone=row.phone,
            tags=row.tags,
            revenue_generated=row.revenue_generated,
        )
        for row in results
    ]
    return customers



class VariantModel(BaseModel):
    title: str
    price: float
    inv_item_qty: int
    weight: int | None = None


@router.get(
    "/get-products", response_model=list[VariantModel], status_code=status.HTTP_200_OK
)
async def get_products(request: Request, db: Session = Depends(get_db)):

    # user = authen    dfklafkdlsfja;ldskfja;skjflsadklfticate_user(request, db)

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(models.Variant).where(models.Variant.shop_id == shop_id)

    results = db.execute(stmt).scalars().all()

    return results


class OwnerModel(BaseModel):
    owner: str
    name: str


@router.get(
    "/get-shop-details", response_model=list[OwnerModel], status_code=status.HTTP_200_OK
)
async def get_shop_details(request: Request, db: Session = Depends(get_db)):

    # user = authen    dfklafkdlsfja;ldskfja;skjflsadklfticate_user(request, db)

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(models.Shop).where(models.Shop.id == shop_id)

    results = db.execute(stmt).scalars().all()

    return results


class OrderModel(BaseModel):
    # id, date, status, qunatity, price
    order_number: int
    timestamp: datetime
    fulfillment_stat: str | None = None
    confirmed: int
    total_price: float


@router.get(
    "/get-orders", response_model=list[OrderModel], status_code=status.HTTP_200_OK
)
async def get_orders(request: Request, db: Session = Depends(get_db)):

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(models.Order).where(models.Order.shop_id == shop_id)

    results = db.execute(stmt).scalars().all()

    return results


class WeekModel(BaseModel):
    total_price: float
    timestamp: datetime
    confirmed: int


@router.get(
    "/get-weeks-data", response_model=list[WeekModel], status_code=status.HTTP_200_OK
)
async def get_week_data(request: Request, db: Session = Depends(get_db)):

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(models.Order).where(models.Order.shop_id == shop_id)

    results = db.execute(stmt).scalars().all()

    return results


class TotalRevenueModel(BaseModel):
    total_price: float
    timestamp: datetime


@router.get(
    "/get-total-revenue",
    response_model=list[TotalRevenueModel],
    status_code=status.HTTP_200_OK,
)
async def get_total_revenue(request: Request, db: Session = Depends(get_db)):

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(models.Order).where(models.Order.shop_id == shop_id)

    results = db.execute(stmt).scalars().all()

    return results


class TotalModel(BaseModel):
    total_revenue: float
    total_customers: int
    total_products: int


@router.get(
    "/get-total",
    response_model=TotalModel,
    status_code=status.HTTP_200_OK,
)
async def get_total(request: Request, db: Session = Depends(get_db)):

    shop_id = Select(models.TenantUser.shop_id).where(
        models.TenantUser.email == mail_default
    )

    stmt = Select(func.count(models.Customer.id)).where(
        models.Customer.shop_id == shop_id
    )

    total_coustomers = db.execute(stmt).scalar_one or 0
    print(total_coustomers)

    stmt = Select(func.count(models.Product.id)).where(
        models.Product.shop_id == shop_id
    )

    total_products = db.execute(stmt).scalar or 0
    print(total_products)

    stmt = Select(func.count(models.Order.total_price)).where(
        models.Order.shop_id == shop_id and models.Order.confirmed == True
    )

    total_revenue = db.execute(stmt).scalar or 0

    total_revenue = round(total_revenue, 2)
    print(total_revenue)

    return TotalModel(
        total_products=total_products,
        total_customers=total_coustomers,
        total_revenue=total_revenue,
    )
