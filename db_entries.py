from db_helpers import (
    insert_shop, insert_tenant_user,
    insert_customer, insert_address,
    insert_product, insert_variant,
    insert_order, insert_line_item
)
from db_helpers import get_db, create_all_tables, clear_entire_database

# Drop n Create Again:
clear_entire_database()
create_all_tables()

# Create a new session
db = next(get_db())

# Shop and TenantUser
shop = insert_shop(
    db=db, id=101, name="My Shop", domain="my.shop.com",
    owner="Alice", email="check@gmail.com"
)
print(shop)

tenant_user = insert_tenant_user(
    db=db, id=201, shop_id=101, email="another@mail.com", pass_hash="hashed_password",
    role="admin", created_at="2025-09-11T12:13:18-04:00", pic_url="http://example.com/pic.jpg"
)
print(tenant_user)

# Customer and Address
customer = insert_customer(
    db=db, id=9319172300000, shop_id=101, timestamp="2025-09-11T12:13:18-04:00",
    first_name="Sarvesh", last_name=None, email="sarvesh@hotmail.com",
    phone=None, tags="vip,main"
)
print(customer)
#in this customer id is 9319172300000, now for making furthur customers,just increment this id by 1


address = insert_address(
    db=db, id=12430558000000, customer_id=301, shop_id=101, company='VIT Chennai',
    address1="Vanadalur-Kelmbakkam Road", address2=None, city="Chennai",
    state="TN", country="India", zip_code="600048", default=True
)
print(address)
##in this address id is 9319172300000, now for making furthur address id,just increment this id by 1

# Product and Variant
product = insert_product(
    db=db, id=10086091500000, shop_id=101, title="Cool T-Shirt", vendor="BrandX",
    product_type="Apparel", slug="cool-tshirt", timestamp="2025-09-11T12:13:18-04:00",
    tags="clothing,summer", status="active"
)
print(product)
#in this product id is 10086091500000, now for making furthur products,just increment this id by 1

variant = insert_variant(
    db=db, id=51146872000000, product_id=10086091500000, shop_id=101, title="Size S",
    price=190, inv_item_id=1001, inv_item_qty=50,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)
variant = insert_variant(
    db=db, id=51146872000001, product_id=10086091500000, shop_id=101, title="Size M",
    price=220, inv_item_id=1002, inv_item_qty=20,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)
variant = insert_variant(
    db=db, id=51146872000002, product_id=10086091500000, shop_id=101, title="Size L",
    price=250, inv_item_id=1003, inv_item_qty=0,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)

# Order and LineItem
order = insert_order(
    db=db, id=7421646000000, customer_id=9319172300000, shop_id=101, order_number=1001,
    confirmed=True, timestamp="2025-09-11T12:13:18-04:00", currency="INR",
    subtotal_price=630, total_discount=50.0, total_tax=20, total_price=600.00,
    financial_stat="paid", fulfillment_stat=None
)
print(order)

line_item = insert_line_item(
    db=db, id=18197211000000, order_id=7421646000000, product_id=10086091500000, shop_id=101,
    variant_id=51146872000001, quantity=2, price=190, total_discount=10.0
)
print(line_item)
line_item = insert_line_item(
    db=db, id=18197211000001, order_id=7421646000000, product_id=10086091500000, shop_id=101,
    variant_id=51146872000001, quantity=1, price=220, total_discount=40.0
)
print(line_item)
