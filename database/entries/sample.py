from database import get_db, clear_entire_database, create_all_tables
from database.insertions import *

# ts = "2025-09-11T12:13:18-04:00"
# print(f"Input: {ts}")
# dt = iso_to_utc(ts)
# print(f"Output: {dt} (UTC naive)")

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
    db=db, id=301, shop_id=101, timestamp="2025-09-11T12:13:18-04:00",
    first_name="Sarvesh", last_name=None, email="sarvesh@hotmail.com",
    phone=None, tags="vip,main"
)
print(customer)

address = insert_address(
    db=db, id=401, customer_id=301, shop_id=101, company='VIT Chennai',
    address1="Vanadalur-Kelmbakkam Road", address2=None, city="Chennai",
    state="TN", country="India", zip_code="600048", default=True
)
print(address)

# Product and Variant
product = insert_product(
    db=db, id=501, shop_id=101, title="Cool T-Shirt", vendor="BrandX",
    product_type="Apparel", slug="cool-tshirt", timestamp="2025-09-11T12:13:18-04:00",
    tags="clothing,summer", status="active"
)
print(product)

variant = insert_variant(
    db=db, id=601, product_id=501, shop_id=101, title="Size S",
    price=190, inv_item_id=1001, inv_item_qty=50,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)
variant = insert_variant(
    db=db, id=602, product_id=501, shop_id=101, title="Size M",
    price=220, inv_item_id=1002, inv_item_qty=20,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)
variant = insert_variant(
    db=db, id=603, product_id=501, shop_id=101, title="Size L",
    price=250, inv_item_id=1003, inv_item_qty=0,
    weight=200, image_url="http://example.com/image.jpg"
)
print(variant)

# Order and LineItem
order = insert_order(
    db=db, id=701, customer_id=301, shop_id=101, order_number=1001,
    confirmed=True, timestamp="2025-09-11T12:13:18-04:00", currency="INR",
    subtotal_price=630, total_discount=50.0, total_tax=20, total_price=600.00,
    financial_stat="paid", fulfillment_stat=None
)
print(order)

line_item = insert_line_item(
    db=db, id=801, order_id=701, product_id=501, shop_id=101,
    variant_id=601, quantity=2, price=190, total_discount=10.0
)
print(line_item)
line_item = insert_line_item(
    db=db, id=802, order_id=701, product_id=501, shop_id=101,
    variant_id=602, quantity=1, price=220, total_discount=40.0
)
print(line_item)


print("\n\n\nWARNING: These entries are not supposed to stay in the database.")
print("Run clear script to remove them.")
