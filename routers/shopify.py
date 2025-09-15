from fastapi import Request, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import models, get_db
import json

router = APIRouter(
    prefix="/shopify",
    tags=["shopify_data"],
)


@router.post("/add-customers")
async def add_shopify(request: Request, db: Session = Depends(get_db)):
    customer_data = await request.json()
    # print(customer_data.id)
    # order_status_url = customer_data["order_status_url"]

    # "https://sarvesh-xeno-store.myshopify.com/95800131877/orders/a8a3c369ab4c7e3dba4c01cb05d03a61/authenticate?key=79e6101bbc4e51708d14102f6991a524"

    # print(customer_data)

    # with open("./3_webhook_customer.json", 'w') as f:
    #     json.dump(customer_data, f)

    customer_model = models.Customer(
        shop_id=95800131877,
        id=customer_data.get("id"),
        timestamp=customer_data.get("created_at"),
        first_name=customer_data.get("first_name"),
        last_name=customer_data.get("last_name"),
        email=customer_data.get("email"),
        phone=customer_data.get("phone"),
        tags=customer_data.get("tags"),
    )
    print(
        f"New Customer: {customer_data.get('id')} - {customer_data.get('first_name')} {customer_data.get('last_name')} added to database.")

    db.add(customer_model)
    db.commit()
    db.refresh(customer_data)


# @app.get("/get-shopify")
# def get_shopify(db: Session = Depends(get_db)):
#     records = db.query(Shopify).all()
#     output = []
#     for record in records:
#         try:
#             output.append(json.loads(str(record.data)))
#         except Exception:
#             output.append({"id": record.id, "error": "Failed to parse data"})
#     return JSONResponse(content=output)
