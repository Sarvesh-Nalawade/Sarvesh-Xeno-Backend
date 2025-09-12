import pytz
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    CHAR,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


# ------------------------------------------------------------------------------
# Base and Constants:
# ------------------------------------------------------------------------------

IST_TIMEZONE = pytz.timezone("Asia/Kolkata")


class Base(DeclarativeBase):
    pass


# ------------------------------------------------------------------------------
# Shop & TenantUsers
# ------------------------------------------------------------------------------

class Shop(Base):
    """Shop Table to store shop details (Multi Tenant Support).
    | Col     | Value Type    |
    |---------|---------------|
    | id      | BIGINT        |
    | name    | VARCHAR(255)  |
    | domain  | VARCHAR(255)  |
    | owner   | VARCHAR(255)  |
    | email   | VARCHAR(255)  |
    """

    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    domain: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (
        Index("idx_shop_name", "name"),
        Index("idx_shop_domain", "domain")
    )

    def __repr__(self) -> str:
        return f"<Shop id={self.id} name={self.name} domain={self.domain} owner={self.owner}>"


class TenantUser(Base):
    """Tenant Users Table to admin users for each shop.
    | Col         | Value Type    |
    |-------------|---------------|
    | id          | BIGINT        |
    | shop_id     | BIGINT        |
    | email       | VARCHAR(255)  |
    | pass_hash   | VARCHAR(255)  |
    | role        | VARCHAR(50)   |
    | pic_url     | VARCHAR(500)  |
    | created_at  | DATETIME      |
    """

    __tablename__ = "tenant_users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    pass_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    pic_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", "shop_id", name="uq_tenant_email_shop"),
        # Index("idx_tenant_users_shop_id", "shop_id"),
        # Index("idx_tenant_users_email", "email") # removed these two as UniqueConstraint under the hood creates composite index for this

    )

    def __repr__(self) -> str:
        return f"<TenantUser id={self.id} email={self.email} shop_id={self.shop_id} role={self.role}>"


# ------------------------------------------------------------------------------
# Data based on Customers.json
# ------------------------------------------------------------------------------

class Customer(Base):
    """Customer Table to store customer details.
    | Col           | Value Type    |
    |---------------|---------------|
    | id            | BIGINT        |
    | shop_id       | BIGINT        |
    | timestamp     | DATETIME      |
    | first_name    | VARCHAR(255)  |
    | last_name     | VARCHAR(255)  |
    | email         | VARCHAR(255)  |
    | phone         | VARCHAR(20)   |
    | tags          | TEXT          |
    """

    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True
    )
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    tags: Mapped[Optional[str]] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("email", "shop_id", name="uq_customer_email_shop"),
        # Index("idx_customer_email", "email"),
        # Index("idx_customer_shop", "shop_id"), # removed this as UniqueConstraint under the hood creates composite index for this
        Index("idx_customer_phone", "phone"),
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.id} name={self.first_name} {self.last_name} email={self.email} shop_id={self.shop_id}>"


class Address(Base):
    """Address Table to store customer addresses.
    | Col           | Value Type    |
    |---------------|---------------|
    | id            | BIGINT        |
    | customer_id   | BIGINT        |
    | shop_id       | BIGINT        |
    | company       | VARCHAR(255)  |
    | address1      | VARCHAR(255)  |
    | address2      | VARCHAR(255)  |
    | city          | VARCHAR(100)  |
    | state         | VARCHAR(100)  |
    | country       | VARCHAR(100)  |
    | zip_code      | VARCHAR(20)   |
    | default       | BOOLEAN       |
    """

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customer.id"), nullable=False, index=True
    )
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True, index=True
    )
    company: Mapped[Optional[str]] = mapped_column(String(255))
    address1: Mapped[str] = mapped_column(String(255), nullable=False)
    address2: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "shop_id", name="uq_address_id_shop"),
    )

    def __repr__(self) -> str:
        return f"<Address id={self.id} customer_id={self.customer_id} shop_id={self.shop_id} city={self.city} country={self.country}>"


# ------------------------------------------------------------------------------
# Data based on Products.json
# ------------------------------------------------------------------------------

class Product(Base):
    """Product Table to store product details.
    | Col           | Value Type    |
    |---------------|---------------|
    | id            | BIGINT        |
    | shop_id       | BIGINT        |
    | title         | VARCHAR(255)  |
    | vendor        | VARCHAR(255)  |
    | product_type  | VARCHAR(100)  |
    | slug          | VARCHAR(255)  |
    | timestamp     | DATETIME      |
    | tags          | TEXT          |
    | status        | VARCHAR(50)   |
    """

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    vendor: Mapped[str] = mapped_column(String(255), nullable=False)
    product_type: Mapped[Optional[str]] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("slug", "shop_id", name="uq_product_slug_shop"),
        Index("idx_product_title", "title"),
        Index("idx_product_vendor", "vendor"),
        # Index("idx_product_slug", "slug"),
        # Index("idx_product_shop", "shop_id"), # removed this as UniqueConstraint under the hood creates composite index for this
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} title={self.title} vendor={self.vendor} shop_id={self.shop_id}>"


class Variant(Base):
    """Variant Table to store product variant details.
    | Col           | Value Type    |
    |---------------|---------------|
    | id            | BIGINT        |
    | product_id    | BIGINT        |
    | shop_id       | BIGINT        |
    | title         | VARCHAR(255)  |
    | price         | DECIMAL(10,2) |
    | inv_item_id   | BIGINT        |
    | inv_item_qty  | INT           |
    | weight        | INT           |
    | image_url     | VARCHAR(500)  |
    """

    __tablename__ = "variant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product.id"), nullable=False, index=True
    )
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    inv_item_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    inv_item_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[Optional[int]] = mapped_column(Integer)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))

    # __table_args__ = (
    # )

    def __repr__(self) -> str:
        return f"<Variant id={self.id} title={self.title} product_id={self.product_id} shop_id={self.shop_id} price={self.price}>"


# ------------------------------------------------------------------------------
# Data based on Orders.json
# ------------------------------------------------------------------------------

class Order(Base):
    """Order Table to store order details.
    | Col             | Value Type    |
    |-----------------|---------------|
    | id              | BIGINT        |
    | customer_id     | BIGINT        |
    | shop_id         | BIGINT        |
    | order_number    | INT           |
    | confirmed       | BOOLEAN       |
    | timestamp       | DATETIME      |
    | currency        | CHAR(3)       |
    | subtotal_price  | DECIMAL(10,2) |
    | total_discount  | DECIMAL(10,2) |
    | total_tax       | DECIMAL(10,2) |
    | total_price     | DECIMAL(10,2) |
    | financial_stat  | VARCHAR(50)   |
    | fulfillment_stat| VARCHAR(50)   |
    """

    __tablename__ = "order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("customer.id"), index=True
    )
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True
    )
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    subtotal_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_discount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_tax: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    financial_stat: Mapped[str] = mapped_column(String(50), nullable=False)
    fulfillment_stat: Mapped[Optional[str]] = mapped_column(String(50))

    __table_args__ = (
        UniqueConstraint("order_number", "shop_id", name="uq_order_number_shop"),
        # Index("idx_order_number", "order_number"),
        # Index("idx_order_shop", "shop_id"), # removed these two as UniqueConstraint under the hood creates composite index for this
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} order_number={self.order_number} shop_id={self.shop_id} total_price={self.total_price}>"


class LineItem(Base):
    """LineItem Table to store order line item details.
    | Col             | Value Type    |
    |-----------------|---------------|
    | id              | BIGINT        |
    | order_id        | BIGINT        |
    | product_id      | BIGINT        |
    | shop_id         | BIGINT        |
    | variant_id      | BIGINT        |
    | quantity        | INT           |
    | price           | DECIMAL(10,2) |
    | total_discount  | DECIMAL(10,2) |
    """

    __tablename__ = "line_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("order.id"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product.id"), nullable=False, index=True
    )
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shop.id"), primary_key=True, index=True
    )
    variant_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_discount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # __table_args__ = (
    # )

    def __repr__(self) -> str:
        return f"<LineItem id={self.id} order_id={self.order_id} product_id={self.product_id} variant_id={self.variant_id} shop_id={self.shop_id} quantity={self.quantity} price={self.price}>"
