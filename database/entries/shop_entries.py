from sqlalchemy.orm import Session
from database.insertions import insert_shop

def insert_all_shops(db: Session):
    """
    Inserts 5 shops into the database.
    - 2 main shops (Xeno + 1 other)
    - 3 other shops
    """
    shops = []
    base_id = 95800131877

    # 1. Main Shop: Xeno Store
    shop1 = insert_shop(
        db=db,
        id=base_id,
        name="Sarvesh Xeno Store",
        domain="sarvesh-xeno-store.myshopify.com",
        owner="Sarvesh Nalawade",
        email="sarvesh.vitchennai@gmail.com"
    )
    shops.append(shop1)
    print(f"Inserted Shop: {shop1.name}")

    # 2. Main Shop: Another main store
    shop2 = insert_shop(
        db=db,
        id=base_id + 1,
        name="The Fashion Hub",
        domain="fashion-hub-india.myshopify.com",
        owner="Priya Sharma",
        email="priya.sharma@fashionhub.in"
    )
    shops.append(shop2)
    print(f"Inserted Shop: {shop2.name}")

    # 3. Additional Shop 1
    shop3 = insert_shop(
        db=db,
        id=base_id + 2,
        name="Urban Organics",
        domain="urban-organics-store.myshopify.com",
        owner="Ravi Kumar",
        email="contact@urbanorganics.in"
    )
    shops.append(shop3)
    print(f"Inserted Shop: {shop3.name}")

    # 4. Additional Shop 2
    shop4 = insert_shop(
        db=db,
        id=base_id + 3,
        name="Home Decor India",
        domain="homedecor-india.myshopify.com",
        owner="Anjali Verma",
        email="support@homedecorindia.com"
    )
    shops.append(shop4)
    print(f"Inserted Shop: {shop4.name}")

    # 5. Additional Shop 3
    shop5 = insert_shop(
        db=db,
        id=base_id + 4,
        name="Digital Art Prints",
        domain="digital-art-prints.myshopify.com",
        owner="Sanjay Patel",
        email="sanjay.patel@digitalart.io"
    )
    shops.append(shop5)
    print(f"Inserted Shop: {shop5.name}")

    return shops

if __name__ == '__main__':
    from database import get_db, clear_entire_database, create_all_tables

    # Recreate the database and tables
    clear_entire_database()
    create_all_tables()

    # Get a new database session
    db_session = next(get_db())

    # Insert all shops
    insert_all_shops(db_session)

    # Close the session
    db_session.close()
