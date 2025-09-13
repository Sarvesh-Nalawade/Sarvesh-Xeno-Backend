import pytz
from datetime import datetime

from typing import Optional
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

IST_TIMEZONE = pytz.timezone('Asia/Kolkata')


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(IST_TIMEZONE), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=None, onupdate=lambda: datetime.now(IST_TIMEZONE)
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} email={self.email}>"
