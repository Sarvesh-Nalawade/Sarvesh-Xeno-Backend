# create.py because I was out of ideas for file name :)

import os
import json
import bcrypt

from database.insertions import (
    insert_shop, insert_tenant_user,
    insert_customer, insert_address,
    insert_product, insert_variant,
    insert_order, insert_line_item
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
    print("\n\n\n⌛ Inserting products data...")
    products = load_json_file('./data_product.json')
    for prod in products:
        resp = insert_product(
            db=db, id=prod['id'], shop_id=prod['shop_id'],
            title=prod['title'], vendor=prod['vendor'],
            slug=prod['slug'], timestamp=prod['timestamp'],
            status=prod['status'], product_type=prod['product_type'],
            tags=prod['tags']
        )
        print(resp)

    # Insert the variants in the database:
    print("\n\n\n⌛ Inserting variants data...")
    variants = load_json_file('./data_variant.json')
    for var in variants:
        resp = insert_variant(
            db=db, id=var['id'], product_id=var['product_id'],
            shop_id=var['shop_id'], title=var['title'],
            price=var['price'], inv_item_id=var['inv_item_id'],
            inv_item_qty=var['inv_item_qty'], weight=var['weight'],
            image_url=var['image_url']
        )
        print(resp)


if __name__ == "__main__":
    clear_entire_database()
    create_all_tables()

    create_entries()
