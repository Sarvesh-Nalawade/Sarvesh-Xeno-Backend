# create.py because I was out of ideas for file name :)

import os
import json
import bcrypt

from database.insertions import (
    insert_shop, insert_tenant_user,
    insert_customer, insert_address,
    # insert_product,  insert_variant,
    # insert_order, insert_line_item
    bulk_insert_products, bulk_insert_variants,
    bulk_insert_orders, bulk_insert_line_items
)

from database import get_db, clear_entire_database, create_all_tables


def hash_string(text: str) -> str:
    encoded = text.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed.decode('utf-8')

# def check_password(text: str, hashed: str) -> bool:
#     return bcrypt.checkpw(text.encode('utf-8'), hashed.encode('utf-8'))


def load_json_file(file_name: str):
    if file_name.startswith('./'):
        file_name = file_name[2:]

    # create absolute path
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    with open(file_path, 'r') as file:
        return json.load(file)


def create_entries():
    db = next(get_db())

    # Insert the shops in the database:
    print("\n\n\n⌛ Inserting shops data...")
    shops = load_json_file('./data_shop.json')
    for shop in shops:
        resp = insert_shop(
            db=db, id=shop['id'], name=shop['name'], domain=shop['domain'],
            owner=shop['owner'], email=shop['email']
        )
        print(resp)

    # Insert the tenant users in the database:
    print("\n\n\n⌛ Inserting tenant users data...")
    tenant_users = load_json_file('./data_tenant_users.json')
    for user in tenant_users:
        resp = insert_tenant_user(
            db=db, id=user['id'], shop_id=user['shop_id'], email=user['email'],
            role=user['role'], created_at=user['timestamp'], pic_url=user['pic_url'],
            pass_hash=hash_string(user['pass_raw'])
        )
        print(resp)

    # Insert the customers in the database:
    print("\n\n\n⌛ Inserting customers data...")
    customers = load_json_file('./data_customer.json')
    for cust in customers:
        resp = insert_customer(
            db=db, id=cust['id'], shop_id=cust['shop_id'],
            first_name=cust['first_name'], last_name=cust['last_name'],
            email=cust['email'], phone=cust['phone'],
            tags=cust['tags'], timestamp=cust['timestamp']
        )
        print(resp)

    # Insert the addresses in the database:
    print("\n\n\n⌛ Inserting addresses data...")
    addresses = load_json_file('./data_address.json')
    for addr in addresses:
        resp = insert_address(
            db=db, id=addr['id'], customer_id=addr['customer_id'],
            shop_id=addr['shop_id'], company=addr['company'],
            address1=addr['address1'], address2=addr['address2'],
            city=addr['city'], state=addr['state'],
            country=addr['country'], zip_code=addr['zip_code'],
            default=addr['default']
        )
        print(resp)

    # Insert the products in the database:
    # print("\n\n\n⌛ Inserting products data...")
    # products = load_json_file('./data_product.json')
    # for prod in products:
    #     resp = insert_product(
    #         db=db, id=prod['id'], shop_id=prod['shop_id'],
    #         title=prod['title'], vendor=prod['vendor'],
    #         slug=prod['slug'], timestamp=prod['timestamp'],
    #         status=prod['status'], product_type=prod['product_type'],
    #         tags=prod['tags']
    #     )
    #     print(resp)

    # Insert the variants in the database:
    # print("\n\n\n⌛ Inserting variants data...")
    # variants = load_json_file('./data_variant.json')
    # for var in variants:
    #     resp = insert_variant(
    #         db=db, id=var['id'], product_id=var['product_id'],
    #         shop_id=var['shop_id'], title=var['title'],
    #         price=var['price'], inv_item_id=var['inv_item_id'],
    #         inv_item_qty=var['inv_item_qty'], weight=var['weight'],
    #         image_url=var['image_url']
    #     )
    #     print(resp)

    # Insert the orders in the database:
    # Too Expensive to insert all orders 1 by 1 [1.5k appx]:
    # print("\n\n\n⌛ Inserting orders data...")
    # orders = load_json_file('./data_order.json')
    # for order in orders:
    #     resp = insert_order(
    #         db=db, id=order['id'], customer_id=order['customer_id'], shop_id=order['shop_id'],
    #         order_number=order['order_number'], confirmed=order['confirmed'],
    #         timestamp=order['timestamp'], currency=order['currency'],
    #         subtotal_price=order['subtotal_price'], total_discount=order['total_discount'],
    #         total_tax=order['total_tax'], total_price=order['total_price'],
    #         financial_stat=order['financial_stat'], fulfillment_stat=order['fulfillment_stat']
    #     )
    #     print(resp)

    # Insert the line items in the database:
    # Too Expensive to insert all line items 1 by 1 [15k appx]:
    # print("\n\n\n⌛ Inserting line items data...")
    # line_items = load_json_file('./data_line_item.json')
    # for item in line_items:
    #     resp = insert_line_item(
    #         db=db, id=item['id'], order_id=item['order_id'],
    #         product_id=item['product_id'], shop_id=item['shop_id'],
    #         variant_id=item['variant_id'], quantity=item['quantity'],
    #         price=item['price'], total_discount=item['total_discount']
    #     )
    #     print(resp)

    # Insert the products in bulk in the database:
    print("\n\n\n⌛ Bulk Inserting products data...")
    products = load_json_file('./data_product.json')
    bulk_insert_products(db=db, products=products, batch_size=30)

    # Insert the variants in bulk in the database:
    print("\n\n\n⌛ Bulk Inserting variants data...")
    variants = load_json_file('./data_variant.json')
    bulk_insert_variants(db=db, variants=variants, batch_size=50)

    # Insert the orders in bulk in the database:
    print("\n\n\n⌛ Bulk Inserting orders data...")
    orders = load_json_file('./data_order.json')
    bulk_insert_orders(db=db, orders=orders, batch_size=500)

    # Insert the line items in bulk in the database:
    print("\n\n\n⌛ Bulk Inserting line items data...")
    line_items = load_json_file('./data_line_item.json')
    bulk_insert_line_items(db=db, line_items=line_items, batch_size=1000)


if __name__ == "__main__":
    clear_entire_database()
    create_all_tables()

    create_entries()
