import hashlib
from sqlalchemy.orm import Session
from database.insertions import insert_tenant_user

def hash_password(password: str) -> str:
    """A simple password hashing function for dummy data."""
    return hashlib.sha256(password.encode()).hexdigest()

def insert_all_tenant_users(db: Session):
    """
    Inserts 10 tenant users into the database.
    - 2 main users from different main shops.
    - 8 other users across all shops.
    """
    tenant_users = []
    
    # Shop IDs from the previously created shops
    main_shop_1_id = 95800131877
    main_shop_2_id = 95800131878
    other_shop_1_id = 95800131879
    other_shop_2_id = 95800131880
    other_shop_3_id = 95800131881

    # Base ID for tenant users
    base_tenant_id = 201

    # 1. Main User for Sarvesh Xeno Store
    user1 = insert_tenant_user(
        db=db, id=base_tenant_id, shop_id=main_shop_1_id,
        email="sarvesh.vitchennai@gmail.com", pass_hash=hash_password("pass123"),
        role="admin", created_at="2025-09-11T12:13:18-04:00",
        pic_url="https://example.com/pic/sarvesh.jpg"
    )
    tenant_users.append(user1)
    print(f"Inserted Tenant User: {user1.email} for Shop ID: {user1.shop_id}")

    # 2. Main User for The Fashion Hub
    user2 = insert_tenant_user(
        db=db, id=base_tenant_id + 1, shop_id=main_shop_2_id,
        email="nalawadesarvesh98@gmail.com", pass_hash=hash_password("pass456"),
        role="admin", created_at="2024-01-16T10:00:00-04:00",
        pic_url="https://example.com/pic/priya.jpg"
    )
    tenant_users.append(user2)
    print(f"Inserted Tenant User: {user2.email} for Shop ID: {user2.shop_id}")

    # 3. Staff for Sarvesh Xeno Store
    user3 = insert_tenant_user(
        db=db, id=base_tenant_id + 2, shop_id=main_shop_1_id,
        email="staff1@xenostore.com", pass_hash=hash_password("staffpass1"),
        role="staff", created_at="2025-09-12T09:30:00-04:00",
        pic_url=None
    )
    tenant_users.append(user3)
    print(f"Inserted Tenant User: {user3.email} for Shop ID: {user3.shop_id}")

    # 4. Staff for The Fashion Hub
    user4 = insert_tenant_user(
        db=db, id=base_tenant_id + 3, shop_id=main_shop_2_id,
        email="support@fashionhub.in", pass_hash=hash_password("staffpass2"),
        role="staff", created_at="2024-02-01T11:00:00-04:00",
        pic_url="https://example.com/pic/support.jpg"
    )
    tenant_users.append(user4)
    print(f"Inserted Tenant User: {user4.email} for Shop ID: {user4.shop_id}")

    # 5. Admin for Urban Organics
    user5 = insert_tenant_user(
        db=db, id=base_tenant_id + 4, shop_id=other_shop_1_id,
        email="ravi.admin@urbanorganics.in", pass_hash=hash_password("orgpass1"),
        role="admin", created_at="2023-11-02T14:00:00-04:00",
        pic_url=None
    )
    tenant_users.append(user5)
    print(f"Inserted Tenant User: {user5.email} for Shop ID: {user5.shop_id}")

    # 6. Staff for Urban Organics
    user6 = insert_tenant_user(
        db=db, id=base_tenant_id + 5, shop_id=other_shop_1_id,
        email="sales@urbanorganics.in", pass_hash=hash_password("orgpass2"),
        role="staff", created_at="2023-11-05T16:20:00-04:00",
        pic_url=None
    )
    tenant_users.append(user6)
    print(f"Inserted Tenant User: {user6.email} for Shop ID: {user6.shop_id}")

    # 7. Admin for Home Decor India
    user7 = insert_tenant_user(
        db=db, id=base_tenant_id + 6, shop_id=other_shop_2_id,
        email="anjali.head@homedecorindia.com", pass_hash=hash_password("decorpass1"),
        role="admin", created_at="2022-05-21T15:00:00-04:00",
        pic_url="https://example.com/pic/anjali.jpg"
    )
    tenant_users.append(user7)
    print(f"Inserted Tenant User: {user7.email} for Shop ID: {user7.shop_id}")

    # 8. Staff for Home Decor India
    user8 = insert_tenant_user(
        db=db, id=base_tenant_id + 7, shop_id=other_shop_2_id,
        email="team@homedecorindia.com", pass_hash=hash_password("decorpass2"),
        role="staff", created_at="2022-06-01T10:10:10-04:00",
        pic_url=None
    )
    tenant_users.append(user8)
    print(f"Inserted Tenant User: {user8.email} for Shop ID: {user8.shop_id}")

    # 9. Admin for Digital Art Prints
    user9 = insert_tenant_user(
        db=db, id=base_tenant_id + 8, shop_id=other_shop_3_id,
        email="sanjay.admin@digitalart.io", pass_hash=hash_password("artpass1"),
        role="admin", created_at="2024-08-11T11:11:11-04:00",
        pic_url="https://example.com/pic/sanjay.jpg"
    )
    tenant_users.append(user9)
    print(f"Inserted Tenant User: {user9.email} for Shop ID: {user9.shop_id}")

    # 10. Staff for Digital Art Prints
    user10 = insert_tenant_user(
        db=db, id=base_tenant_id + 9, shop_id=other_shop_3_id,
        email="artist-relations@digitalart.io", pass_hash=hash_password("artpass2"),
        role="staff", created_at="2024-08-12T12:12:12-04:00",
        pic_url=None
    )
    tenant_users.append(user10)
    print(f"Inserted Tenant User: {user10.email} for Shop ID: {user10.shop_id}")

    return tenant_users

if __name__ == '__main__':
    from database import get_db, clear_entire_database, create_all_tables
    from database.entries.shop_entries import insert_all_shops

    # Recreate the database and tables
    clear_entire_database()
    create_all_tables()

    # Get a new database session
    db_session = next(get_db())

    # Insert shops first to satisfy foreign key constraints
    print("--- Inserting Shops ---")
    insert_all_shops(db_session)
    
    # Insert tenant users
    print("\n--- Inserting Tenant Users ---")
    insert_all_tenant_users(db_session)

    # Close the session
    db_session.close()
