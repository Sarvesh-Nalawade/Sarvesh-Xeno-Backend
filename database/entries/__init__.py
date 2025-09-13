import os
from dotenv import load_dotenv

from database.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# ------------------------------------------------------------------------------
# Base and Constants:
# ------------------------------------------------------------------------------

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", None)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_DATABASE", "xeno_shopify")
DB_CHAR = os.getenv("DB_CHARSET", "utf8mb4")
VERBOSE = os.getenv("DB_VERBOSE", "true").lower() == "true"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHAR}"

engine = create_engine(DATABASE_URL, echo=VERBOSE, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ------------------------------------------------------------------------------
# Base Functions:
# ------------------------------------------------------------------------------

def get_db():
    """Provide a transactional session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear_entire_database():
    """Drops all tables in the database."""
    Base.metadata.drop_all(bind=engine)
    print("⚠️  Cleared Entire DB")


def create_all_tables():
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("✅ Created All Tables")
