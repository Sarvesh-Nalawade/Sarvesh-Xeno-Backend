from typing import Any, Dict, List
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from db_models import Base, User
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", None)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_DATABASE", "xeno_shopify")
DB_CHAR = os.getenv("DB_CHARSET", "utf8mb4")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHAR}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

# Proper session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


# ---- UTILS ----
def create_tables() -> None:
    Base.metadata.create_all(engine)
    print("✅ All tables created.")


def drop_all_tables() -> None:
    Base.metadata.drop_all(engine)
    print("⚠️ All tables dropped.")


def insert_users(data: List[Dict[str, Any]]) -> None:
    with SessionLocal() as session:
        users = [User(**row) for row in data]
        session.add_all(users)
        session.commit()
        print(f"✅ Inserted {len(users)} users.")


def get_all_users() -> None:
    with SessionLocal() as session:
        users = session.query(User).all()
        if users:
            for user in users:
                print(user)
        else:
            print("No users found.")


if __name__ == "__main__":
    drop_all_tables()   # ensure clean state for testing
    create_tables()

    sample_users = [
        {"username": "Bhushan Songire", "email": "bbs@gmail.com", "hashed_password": "hashed_pass_123"},
        {"username": "Sarvesh Kumar", "email": "sadfasd@gmail.com", "hashed_password": "hashed_pass_456"},
    ]

    insert_users(sample_users)
    get_all_users()
