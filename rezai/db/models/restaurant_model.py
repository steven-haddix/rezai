from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from rezai.db.base import Base

if TYPE_CHECKING:
    from .group_restaurant_model import GroupRestaurant  # noqa: WPS300


class Restaurant(Base):
    """Model for storing restaurant search results."""

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=255))
    type: Mapped[str] = mapped_column(String(length=100))
    category: Mapped[str] = mapped_column(String(length=100))
    website: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(String(length=1000))
    address: Mapped[str] = mapped_column(String(length=255))
    phone: Mapped[str] = mapped_column(String(length=20))
    rating: Mapped[float] = mapped_column(Integer)
    reviews: Mapped[int] = mapped_column(Integer)
    unclaimed: Mapped[bool] = mapped_column(Boolean)
    hours: Mapped[str] = mapped_column(String(length=1000))
    opening_hours: Mapped[str] = mapped_column(String(length=1000))
    people_also_search_for: Mapped[str] = mapped_column(String(length=1000))
    menu: Mapped[str] = mapped_column(String(length=1000))
    reservations: Mapped[str] = mapped_column(String(length=1000))
    order: Mapped[str] = mapped_column(String(length=1000))
    order_food: Mapped[str] = mapped_column(String(length=1000))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    group_restaurants: Mapped[List["GroupRestaurant"]] = relationship(  # type: ignore
        "GroupRestaurant",
        back_populates="restaurant",
    )
