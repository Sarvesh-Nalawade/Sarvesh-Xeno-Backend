from typing import Optional
from sqlalchemy.orm import Session

from database.models import (
    Shop, TenantUser,
    Customer, Address, Product,
    Variant, Order, LineItem
)

from database.utils import iso_to_utc


# ------------------------------------------------------------------------------
# Insert: Shop and TenantUser
# ------------------------------------------------------------------------------

def insert_shop(db: Session, id: int, name: str, domain: str, owner: str, email: str) -> Shop:
    """Insert a new Shop row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Shop ID.
        name (str): Shop name.
        domain (str): Shop domain.
        owner (str): Shop owner name.
        email (str): Shop/Owner email.
    Returns:
        Shop: The newly created Shop object.
    """

    shop = Shop(id=id, name=name, domain=domain, owner=owner, email=email)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop


def insert_tenant_user(
        db: Session, id: int, shop_id: int, email: str, pass_hash: str,
        role: str, created_at: str, pic_url: Optional[str] = None
) -> TenantUser:
    """Insert a new TenantUser row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): TenantUser ID.
        shop_id (int): Associated Shop ID.
        email (str): User email.
        pass_hash (str): Password hash.
        role (str): User role (e.g., 'admin', 'staff').
        created_at (str): ISO-8601 timestamp string for creation time `2025-09-11T12:13:18-04:00`.
        pic_url (Optional[str]): URL to user's profile picture. Default is None.
    Returns:
        TenantUser: The newly created TenantUser object.
    """

    tenant_user = TenantUser(
        id=id, shop_id=shop_id, email=email, pass_hash=pass_hash,
        role=role, pic_url=pic_url, created_at=iso_to_utc(created_at))
    db.add(tenant_user)
    db.commit()
    db.refresh(tenant_user)
    return tenant_user


# ------------------------------------------------------------------------------
# Insert: Customer and Address
# ------------------------------------------------------------------------------

def insert_customer(
        db: Session, id: int, shop_id: int, timestamp: str, first_name: str,
        last_name: Optional[str] = None, email: Optional[str] = None,
        phone: Optional[str] = None, tags: Optional[str] = None
) -> Customer:
    """Insert a new Customer row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Customer ID.
        shop_id (int): Associated Shop ID.
        timestamp (str): ISO-8601 timestamp string for customer creation.
        first_name (str): Customer's first name.
        last_name (Optional[str]): Customer's last name. Default is None.
        email (Optional[str]): Customer's email. Default is None.
        phone (Optional[str]): Customer's phone number. Default is None.
        tags (Optional[str]): Customer tags (comma separated). Default is None.
    Returns:
        Customer: The newly created Customer object.
    """

    customer = Customer(
        id=id, shop_id=shop_id, timestamp=iso_to_utc(timestamp),
        first_name=first_name, last_name=last_name, email=email,
        phone=phone, tags=tags)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def insert_address(
        db: Session, id: int, customer_id: int, shop_id: int, address1: str,
        city: str, country: str, zip_code: str, company: Optional[str] = None,
        address2: Optional[str] = None, state: Optional[str] = None,
        default: bool = False
) -> Address:
    """Insert a new Address row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Address ID.
        customer_id (int): Associated Customer ID.
        shop_id (int): Associated Shop ID.
        company (Optional[str]): Company name. Default is None.
        address1 (str): Primary address line.
        address2 (Optional[str]): Secondary address line. Default is None.
        city (str): City of the address.
        state (Optional[str]): State or province. Default is None.
        country (str): Country of the address.
        zip_code (str): ZIP or postal code.
        default (bool): Whether this is the default address. Default is False.
    Returns:
        Address: The newly created Address object.
    """

    address = Address(
        id=id, customer_id=customer_id, shop_id=shop_id, company=company,
        address1=address1, address2=address2, city=city, state=state,
        country=country, zip_code=zip_code, default=default)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


# ------------------------------------------------------------------------------
# Insert: Product and Variant
# ------------------------------------------------------------------------------

def insert_product(
        db: Session, id: int, shop_id: int, title: str, vendor: str,
        slug: str, timestamp: str, status: str,
        product_type: Optional[str] = None, tags: Optional[str] = None
) -> Product:
    """Insert a new Product row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Product ID.
        shop_id (int): Associated Shop ID.
        title (str): Product title.
        vendor (str): Vendor name.
        slug (str): Product slug (unique per shop).
        timestamp (str): ISO-8601 timestamp string for product creation.
        status (str): Product status (e.g., 'active', 'archived').
        product_type (Optional[str]): Product type. Default is None.
        tags (Optional[str]): Product tags. Default is None.
    Returns:
        Product: The newly created Product object.
    """
    product = Product(
        id=id, shop_id=shop_id, title=title, vendor=vendor,
        product_type=product_type, slug=slug, timestamp=iso_to_utc(timestamp),
        tags=tags, status=status)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def insert_variant(
        db: Session, id: int, product_id: int, shop_id: int, title: str,
        price: float, inv_item_id: int, inv_item_qty: int,
        weight: Optional[int] = None, image_url: Optional[str] = None
) -> Variant:
    """Insert a new Variant row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Variant ID.
        product_id (int): Associated Product ID.
        shop_id (int): Associated Shop ID.
        title (str): Variant title.
        price (float): Variant price.
        inv_item_id (int): Inventory item ID.
        inv_item_qty (int): Inventory quantity.
        weight (Optional[int]): Weight of the variant. Default is None.
        image_url (Optional[str]): Image URL. Default is None.
    Returns:
        Variant: The newly created Variant object.
    """

    variant = Variant(
        id=id, product_id=product_id, shop_id=shop_id, title=title,
        price=price, inv_item_id=inv_item_id, inv_item_qty=inv_item_qty,
        weight=weight, image_url=image_url)
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


# ------------------------------------------------------------------------------
# Insert: Order and LineItem
# ------------------------------------------------------------------------------

def insert_order(
        db: Session, id: int, shop_id: int, order_number: int,
        confirmed: bool, timestamp: str, currency: str, subtotal_price: float,
        total_discount: float, total_tax: float, total_price: float,
        financial_stat: str, customer_id: Optional[int] = None,
        fulfillment_stat: Optional[str] = None
) -> Order:
    """Insert a new Order row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): Order ID.
        customer_id (Optional[int]): Associated Customer ID. Default is None.
        shop_id (int): Associated Shop ID.
        order_number (int): Order number (unique per shop).
        confirmed (bool): Whether the order is confirmed.
        timestamp (str): ISO-8601 timestamp string for order creation.
        currency (str): Currency code (e.g., 'INR').
        subtotal_price (float): Subtotal price of the order.
        total_discount (float): Total discount applied.
        total_tax (float): Total tax applied.
        total_price (float): Final total price.
        financial_stat (str): Financial status (e.g., 'paid').
        fulfillment_stat (Optional[str]): Fulfillment status. Default is None.
    Returns:
        Order: The newly created Order object.
    """
    order = Order(
        id=id, customer_id=customer_id, shop_id=shop_id,
        order_number=order_number, confirmed=confirmed,
        timestamp=iso_to_utc(timestamp), currency=currency,
        subtotal_price=subtotal_price, total_discount=total_discount,
        total_tax=total_tax, total_price=total_price,
        financial_stat=financial_stat, fulfillment_stat=fulfillment_stat)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def insert_line_item(
        db: Session, id: int, order_id: int, product_id: int,
        shop_id: int, variant_id: int, quantity: int, price: float,
        total_discount: float
) -> LineItem:
    """Insert a new LineItem row and return the object.
    Args:
        db (Session): SQLAlchemy session object.
        id (int): LineItem ID.
        order_id (int): Associated Order ID.
        product_id (int): Associated Product ID.
        shop_id (int): Associated Shop ID.
        variant_id (int): Associated Variant ID.
        quantity (int): Quantity ordered.
        price (float): Price per item.
        total_discount (float): Discount applied to the line item.
    Returns:
        LineItem: The newly created LineItem object.
    """
    line_item = LineItem(
        id=id, order_id=order_id, product_id=product_id,
        shop_id=shop_id, variant_id=variant_id, quantity=quantity,
        price=price, total_discount=total_discount)
    db.add(line_item)
    db.commit()
    db.refresh(line_item)
    return line_item


# ------------------------------------------------------------------------------
# Simple Tests:
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Run the script:
    print("Please run: `python -m database.entries.sample_insertions`")
    