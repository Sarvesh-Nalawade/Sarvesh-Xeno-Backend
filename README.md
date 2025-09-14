# Index:
1. [Database](#database)
    1. [Initialization](#initialization)
    2. [Schema](#schema)
    3. [Data Extraction](#data-extraction)
        1. [Shop Table](#shop-table)
        2. [TenantUsers Table](#tenantusers-table)
        3. [Customer Table](#customer-table)
        4. [Address Table](#address-table)
        5. [Product Table](#product-table)
        6. [Variant Table](#variant-table)
        7. [Order Table](#order-table)
        8. [LineItem Table](#lineitem-table)
2. [Others](#others)


---


# Database:

## Initialization:
1. First Login to existing connection.
    - Locally I am using MySQL Workbench.
    - Dev Env - MySQL v 8.0.40

2. Create new database for this project:
    ```sql
    CREATE DATABASE IF NOT EXISTS `xeno_shopify` DEFAULT CHARACTER SET utf8mb4;
    ```

3. Verify database creation and use it:
    ```sql
    SHOW DATABASES;
    USE xeno_shopify;
    ```

4. See all the tables in the database (should be empty initially):
    ```sql
    SHOW TABLES;
    ```

5. To initialize the database tables, run:
    ```bash
    python -m database.entries.initialize
    ```

6. To make some sample entries and see the db:
    ```bash
    python -m database.entries.sample
    ```

7. To SEE the database:
    ```bash
    python mini_codes/sql_db/mysql_to_sqlite.py
    ```
    Then, open the 'temp_check.db' file using SQLite Viewer or any SQLite client.

8. To clear the database (all tables and data):
    ```bash
    python -m database.entries.clear
    ```

9. To make all initial (synthetic) entries, run:
    ```bash
    python -m database.entries.synthetic
    ```


## Design:

1. The Shopify API returns response under these categories:
    - Products
    - Orders
    - Customers
    - Carts (not used currently)
    - Checkouts (not used currently)
    - Shop (metadata about the shop, used for multi-tenancy)

2. Out of these, I manually checked each individual key and decided to store only the relevant ones in our database.
3. The relevant data needs conversion from NoSQL (JSON) to SQL (Tables).

4. The tables are designed in a way to minimize redundancy and optimize relationships using Foreign Keys. These are the tables I designed:
    1. Customer
    2. Address
    3. Product
    4. Variant
    5. Order
    6. LineItem

5. Additionally for multi-tenancy, these two tables are added:
    1. Shop  
    2. TenantUsers  
    This allows, multiple shops and multiple authorized people per shop to see dashboard.


---

## Schema:

> [!IMPORTANT]  
> Any change made in Schema must be reflected in three places - 1. This README 2. db_models.py functions 3. db_models.py Docstring declarations 

**Timestamp Note**:
- Shopify gives timestamps with tz, but for storage, I will always use UTC and store as DATETIME (without tz info) in MySQL.
- So, all timestamps must be (in Python) converted to UTC before storing in DB.

**Multi-Tenancy Note**:
1. Primary Key:
    - All business tables (Customer, Address, Product, Variant, Order, LineItem) use a composite primary key `(shop_id, id)` to prevent collisions across stores.  
    - So, if you see PK in two columns, it means both together form the primary key.  

2. Foreign Key:
    - All foreign keys are also scoped by `shop_id`
    - e.g. `(shop_id, customer_id)` → Customer
    - e.g. `(shop_id, product_id)` → Product.  

3. Unique constraints:
    - All uniques in business tables are scoped by `shop_id`
    - Customer.email -> UNIQUE(email, shop_id)
    - Product.slug -> UNIQUE(slug, shop_id)
    - Order.order_number -> UNIQUE(order_number, shop_id)

**Tables:**


1. Shop Table:
    - For multi-tenancy, each Shop will have its own API key and data.
    - s is a single shop's JSON object from the response of the Shopify API for `shop.json`.
    - | Col     | Value Type    | constr    | location |
      |---------|---------------|-----------|----------|
      | id      | BIGINT        | PK        | s.id |
      | name    | VARCHAR(255)  | NN, UNIQUE| s.name |
      | domain  | VARCHAR(255)  | NN, UNIQUE| s.domain |
      | owner   | VARCHAR(255)  | NN        | s.shop_owner |
      | email   | VARCHAR(255)  | NN        | s.email |
    - Index:
        - Shop.domain (already unique).
        - Shop.name (non-unique index, for search).
    - Note: This table will be referenced by all other tables via a foreign key (shop_id) to ensure data isolation between different shops.


2. TenantUsers Table:
    - To manage multiple users who can access the dashboard for a single shop.
    - Data will be obtained from our own user management system, not from Shopify.
    - | Col         | Value Type    | constr    |
      |-------------|---------------|-----------|
      | id          | BIGINT        | PK        |
      | shop_id     | BIGINT        | FK        |
      | email       | VARCHAR(255)  | NN        |
      | pass_hash   | VARCHAR(255)  | NN        |
      | role        | VARCHAR(50)   | NN        |
      | pic_url     | VARCHAR(500)  | nullable  |
      | created_at  | DATETIME      | NN        |
    - Constraint:
        - UNIQUE(email, shop_id) to allow same email for different shops.
    - Index:
        - TenantUsers.shop_id (FK lookup).
        - TenantUsers.email (already unique).


3. Customer Table:  
    - Assume c to be a single customer JSON object from the customers array in the Shopify API response for `customers.json`.
    - | Col           | Value Type    | constr    | location |
      |---------------|---------------|-----------|----------|
      | id            | BIGINT        | PK        | c.id |
      | shop_id       | BIGINT        | FK, PK    | #DecideSrcLater |
      | timestamp     | DATETIME      | NN        | c.created_at |
      | first_name    | VARCHAR(255)  | NN        | c.first_name |
      | last_name     | VARCHAR(255)  | nullable  | c.last_name |
      | email         | VARCHAR(255)  | NULL      | c.email |
      | phone         | VARCHAR(20)   | nullable  | c.phone |
      | tags          | TEXT          | nullable  | c.tags |
    - Constraint:
        - Email unique constraint is UNIQUE(email, shop_id) but allows multiple NULLs. 
        - [SQL treats (NULL, shop_1) and (NULL, shop_2) as different values]
        - Basically, NULLs are counted Distinct.
    - Index: 
        - Customer.email (partial unique where not null).
        - Customer.phone (non-unique index, for fast lookup).
        - Customer.shop_id (foreign key lookup).
    - Note:
        - Timestamp of Shopify is like `2023-08-15T10:20:30-04:00` (with timezone info), 
        - I will convert this to UTC in Python
        - And then store it as DATETIME in MySQL (which does not store timezone info).
        - Composite Primary Key (id, shop_id) to ensure uniqueness across multiple shops.


4. Address Table:
    - Each customer can have multiple addresses, hence a separate table with a foreign key relationship to the Customer table.
    - cd is one single address object from the `addresses` array inside c.
    - Make sure that code must iterate over all items in [] and store each add.
    - | Col           | Value Type    | constr    | location |
      |---------------|---------------|-----------|----------|
      | id            | BIGINT        | PK        | cd.id |
      | customer_id   | BIGINT        | FK        | cd.customer_id |
      | shop_id       | BIGINT        | FK, PK    | #DecideSrcLater |
      | company       | VARCHAR(255)  | nullable  | cd.company |
      | address1      | VARCHAR(255)  | NN        | cd.address1 |
      | address2      | VARCHAR(255)  | nullable  | cd.address2 |
      | city          | VARCHAR(100)  | NN        | cd.city |
      | state         | VARCHAR(100)  | nullable  | cd.province |
      | country       | VARCHAR(100)  | NN        | cd.country |
      | zip_code      | VARCHAR(20)   | NN        | cd.zip |
      | default       | BOOLEAN       | def=False | cd.default |
    - Constraint:
        - Composite unique constraint is UNIQUE(id, customer_id, shop_id) to ensure uniqueness across multiple shops.
    - Index:
        - Address.customer_id (foreign key lookup).
        - Address.city (non-unique index, for analytics queries).
        - Address.shop_id (foreign key lookup).
    - I was planning `pin_code CHAR(6)` but some countries have alphanumeric postal codes, so changed to `zip_code VARCHAR(20)`.
        

5. Product Table:
    - p is a single product JSON object from the products array in the Shopify API response for `products.json`.
    - There can be multiple variants for a single product, hence a separate Variant table with a foreign key relationship to the Product table.
    - | Col           | Value Type    | constr    | location |
      |---------------|---------------|-----------|----------|
      | id            | BIGINT        | PK        | p.id |
      | shop_id       | BIGINT        | FK, PK    | #DecideSrcLater |
      | title         | VARCHAR(255)  | NN        | p.title |
      | vendor        | VARCHAR(255)  | NN        | p.vendor |
      | product_type  | VARCHAR(100)  | nullable  | p.product_type |
      | slug          | VARCHAR(255)  | NN        | p.handle |
      | timestamp     | DATETIME      | NN        | p.created_at |
      | tags          | TEXT          | nullable  | p.tags |      
      | status        | VARCHAR(50)   | NN        | p.status |
    - Constraint:
        - Slug unique constraint is UNIQUE(slug, shop_id) to allow same slug for different shops.
    - Index:
        - Product.slug (already unique).
        - Product.title (non-unique index, for search).
        - Product.vendor (non-unique index, for analytics queries).
        - Product.shop_id (FK lookup).
        
6. Variant Table:
    - v is a single variant JSON object from the `variants` array inside p.
    - Make sure that code must iterate over all items in [] and store each var.
    - | Col           | Value Type    | constr    | location |
      |---------------|---------------|-----------|----------|
      | id            | BIGINT        | PK        | v.id |
      | product_id    | BIGINT        | FK        | v.product_id |
      | shop_id       | BIGINT        | FK, PK    | #DecideSrcLater |
      | title         | VARCHAR(255)  | NN        | v.title |
      | price         | DECIMAL(10,2) | NN        | v.price (str in json) |
      | inv_item_id   | BIGINT        | NN        | v.inventory_item_id |
      | inv_item_qty  | INT           | NN        | v.inventory_quantity |
      | weight        | INT           | nullable  | v.grams |
      | image_url     | VARCHAR(500)  | nullable  | see note_1 below |
    - note_1 : First get the v.image_id, then return 'src' key of JSON obj in p.images array having id = v.image_id, only first one (as multiple can exist maybe)
    - Wight (gram) is INT as Shopify gives it as whole number in grams.
    - Index:
        - Variant.product_id (FK lookup).
        - Variant.shop_id (FK lookup).


7. Order Table:
    - o is a single order JSON object from the orders array in the Shopify API response for `orders.json`.
    - Each order can have multiple line items, hence a separate LineItem table with a foreign key relationship to the Order table.
    - | Col             | Value Type    | constr    | location |
      |-----------------|---------------|-----------|----------|
      | id              | BIGINT        | PK        | o.id |
      | customer_id     | BIGINT        | FK, nullable | o.customer.id (can be null for guest checkouts) |
      | shop_id         | BIGINT        | FK, PK    | #DecideSrcLater |
      | order_number    | INT           | NN        | o.order_number |
      | confirmed       | BOOLEAN       | NN        | o.confirmed |
      | timestamp       | DATETIME      | NN        | o.created_at |
      | currency        | CHAR(3)       | NN        | o.currency |
      | subtotal_price  | DECIMAL(10,2) | NN        | o.subtotal_price (str in json) |
      | total_discount  | DECIMAL(10,2) | NN        | o.total_discounts (str in json) |
      | total_tax       | DECIMAL(10,2) | NN        | o.total_tax (str in json) |
      | total_price     | DECIMAL(10,2) | NN        | o.total_price (str in json) |
      | financial_stat  | VARCHAR(50)   | NN        | o.financial_status |
      | fulfillment_stat| VARCHAR(50)   | nullable  | o.fulfillment_status |
    - Constraint:
        - Order unique constraint is UNIQUE(order_number, shop_id) to allow same order_number for different shops.
    - Index:
        - Order.order_number (already unique).
        - Order.customer_id (FK lookup).
        - Order.shop_id (FK lookup).
        - Order.timestamp (for time-based queries).
        

8. LineItem Table:
    - oi is a single line item JSON object from the `line_items` array inside o.
    - Make sure that code must iterate over all items in [] and store each line item.
    - | Col             | Value Type    | constr    | location |
      |-----------------|---------------|-----------|----------|
      | id              | BIGINT        | PK        | oi.id |
      | order_id        | BIGINT        | FK        | oi.order_id |
      | product_id      | BIGINT        | FK        | oi.product_id |
      | shop_id         | BIGINT        | FK, PK    | #DecideSrcLater |
      | variant_id      | BIGINT        | NN        | oi.variant_id |
      | quantity        | INT           | NN        | oi.quantity |
      | price           | DECIMAL(10,2) | NN        | oi.price (str in json) |
      | total_discount  | DECIMAL(10,2) | NN        | oi.total_discount (str in json) |
    - Constraint:
        - Composite unique constraint is UNIQUE(order_id, product_id, variant_id) to avoid duplicate line items for same product variant in an order.
        - No, but removing this as it might cause issue in case of multiple same variant in one order due to partial fulfillment etc.
    - Index:
        - LineItem.order_id (FK lookup).
        - LineItem.product_id (FK lookup).
        - LineItem.variant_id (FK lookup).
        - LineItem.shop_id (FK lookup).
    - Keeping shop_id here is redundant as we can trace back order_id > order > shop, 
    - but it will speed up queries for multi-tenant setup.
    - also, given short timeline, I will denormalize a bit for easy queries.

---


# Others:
webhook event version = 2025-07

# HTTPS:



# HTTPS Cert:

1. [Install OpenSSL](https://slproweb.com/products/Win32OpenSSL.html)
    - PATH: `C:\Program Files\OpenSSL-Win64`

2. Created file: `C:\Program Files\OpenSSL-Win64\bin\openssl.cnf`
    ```
    # Minimal OpenSSL configuration file
    [ req ]
    distinguished_name = req_distinguished_name
    x509_extensions = v3_req
    prompt = no

    [ req_distinguished_name ]
    CN = localhost

    [ v3_req ]
    subjectAltName = @alt_names

    [ alt_names ]
    DNS.1 = localhost
    ```

3. Create self-signed cert:
    ```powershell
    openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost" -config "C:\Program Files\OpenSSL-Win64\bin\openssl.cnf"
    
    openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" -config "C:\Program Files\OpenSSL-Win64\bin\openssl.cnf"
    ```

5. Export:
    ```powershell
    openssl x509 -in cert.pem -out cert.crt
    ```

4. Run FastAPI with HTTPS:
    ```powershell
    uvicorn main:app --host 127.0.0.1 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
    ```
