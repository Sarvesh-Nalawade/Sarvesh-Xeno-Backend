import random
from faker import Faker
from sqlalchemy.orm import Session
from database.insertions import insert_customer
from datetime import datetime, timedelta

def generate_random_timestamp(start_date, end_date):
    """Generates a random ISO-8601 timestamp within a date range."""
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.isoformat() + "Z"

def insert_all_customers(db: Session):
    """
    Inserts 70 customers into the database.
    - 20 customers for each of the 2 main shops.
    - 10 customers for each of the 3 other shops.
    """
    fake = Faker('en_IN')
    customers = []
    
    # Shop IDs
    main_shop_ids = [95800131877, 95800131878]
    other_shop_ids = [95800131879, 95800131880, 95800131881]
    
    # Base customer ID
    customer_id_counter = 9319172300000
    
    # Date range for timestamps
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 9, 1)

    # Insert 20 customers for each of the 2 main shops
    for shop_id in main_shop_ids:
        for i in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            customer = insert_customer(
                db=db,
                id=customer_id_counter,
                shop_id=shop_id,
                timestamp=generate_random_timestamp(start_date, end_date),
                first_name=first_name,
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}{i}@{fake.free_email_domain()}",
                phone=fake.phone_number(),
                tags=random.choice([None, "VIP", "New", "Returning,VIP"])
            )
            customers.append(customer)
            customer_id_counter += 1
    print(f"Inserted 40 customers for the 2 main shops.")

    # Insert 10 customers for each of the 3 other shops
    for shop_id in other_shop_ids:
        for i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            customer = insert_customer(
                db=db,
                id=customer_id_counter,
                shop_id=shop_id,
                timestamp=generate_random_timestamp(start_date, end_date),
                first_name=first_name,
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}{i}@{fake.free_email_domain()}",
                phone=fake.phone_number(),
                tags=random.choice([None, "Test"])
            )
            customers.append(customer)
            customer_id_counter += 1
    print(f"Inserted 30 customers for the 3 other shops.")

    return customers

if __name__ == '__main__':
    from database import get_db, clear_entire_database, create_all_tables
    from database.entries.shop_entries import insert_all_shops
    from database.entries.tenant_user_entries import insert_all_tenant_users

    # Recreate the database and tables
    clear_entire_database()
    create_all_tables()

    # Get a new database session
    db_session = next(get_db())

    # Insert prerequisite data
    print("--- Inserting Shops ---")
    insert_all_shops(db_session)
    print("\n--- Inserting Tenant Users ---")
    insert_all_tenant_users(db_session)
    
    # Insert customers
    print("\n--- Inserting Customers ---")
    insert_all_customers(db_session)

    # Close the session
    db_session.close()
