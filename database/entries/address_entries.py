import random
from faker import Faker
from sqlalchemy.orm import Session
from database.models import Customer
from database.insertions import insert_address

def insert_all_addresses(db: Session):
    """
    Inserts an address for every customer in the database.
    - For the 2 main shops, addresses are distributed across 5 states and 10 cities.
    - For the 3 other shops, addresses are generated randomly.
    """
    fake = Faker('en_IN')
    addresses = []
    
    # Shop IDs
    main_shop_ids = [95800131877, 95800131878]
    
    # Predefined states and cities for main shops
    indian_locations = {
        "Maharashtra": ["Mumbai", "Pune"],
        "Delhi": ["New Delhi", "North Delhi"],
        "Karnataka": ["Bengaluru", "Mysuru"],
        "Tamil Nadu": ["Chennai", "Coimbatore"],
        "West Bengal": ["Kolkata", "Howrah"]
    }
    states = list(indian_locations.keys())

    # Get all customers from the database
    all_customers = db.query(Customer).all()
    if not all_customers:
        print("No customers found in the database. Please insert customers first.")
        return []

    # Base address ID
    address_id_counter = 12430558000000

    for customer in all_customers:
        is_main_shop_customer = customer.shop_id in main_shop_ids
        
        if is_main_shop_customer:
            # Randomly select from the predefined 5 states and 10 cities
            state = random.choice(states)
            city = random.choice(indian_locations[state])
            zip_code = fake.postcode() # Faker can generate a plausible zip for the region
            address1 = fake.street_address()
        else:
            # Generate any random Indian address for other shops
            state = fake.state()
            city = fake.city()
            zip_code = fake.postcode()
            address1 = fake.street_address()

        address = insert_address(
            db=db,
            id=address_id_counter,
            customer_id=customer.id,
            shop_id=customer.shop_id,
            address1=address1,
            city=city,
            state=state,
            country="India",
            zip_code=zip_code,
            company=fake.company() if random.choice([True, False]) else None,
            default=True 
        )
        addresses.append(address)
        address_id_counter += 1

    print(f"Inserted {len(addresses)} addresses for {len(all_customers)} customers.")
    return addresses

if __name__ == '__main__':
    from database import get_db, clear_entire_database, create_all_tables
    from database.entries.shop_entries import insert_all_shops
    from database.entries.tenant_user_entries import insert_all_tenant_users
    from database.entries.customer_entries import insert_all_customers

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
    print("\n--- Inserting Customers ---")
    insert_all_customers(db_session)
    
    # Insert addresses
    print("\n--- Inserting Addresses ---")
    insert_all_addresses(db_session)

    # Close the session
    db_session.close()
