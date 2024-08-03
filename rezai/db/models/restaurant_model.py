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
    website: Mapped[str] = mapped_column(String(length=255), nullable=True)
    description: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    address: Mapped[str] = mapped_column(String(length=255), nullable=True)
    phone: Mapped[str] = mapped_column(String(length=20), nullable=True)
    rating: Mapped[float] = mapped_column(Integer, nullable=True)
    reviews: Mapped[int] = mapped_column(Integer, nullable=True)
    unclaimed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    hours: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    opening_hours: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    people_also_search_for: Mapped[str] = mapped_column(
        String(length=1000),
        nullable=True,
    )
    menu: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    reservations: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    order: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    order_food: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Add server_default to set a default value
        onupdate=func.now(),
        default=func.now(),
    )
    group_restaurants: Mapped[List["GroupRestaurant"]] = relationship(  # type: ignore
        "GroupRestaurant",
        back_populates="restaurant",
        foreign_keys="GroupRestaurant.restaurant_id",
    )
