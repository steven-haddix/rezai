from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, Integer

from rezai.db.base import Base

if TYPE_CHECKING:
    from .restaurant_model import Restaurant  # noqa: WPS300


class GroupRestaurant(Base):
    """Model for storing group restaurants and individual ratings."""

    __tablename__ = "group_restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
    )
    restaurant: Mapped["Restaurant"] = relationship(  # noqa: F821
        "Restaurant",
        back_populates="group_restaurants",
    )
    ratings: Mapped[List["GroupRestaurantRating"]] = relationship(
        "GroupRestaurantRating",
        back_populates="group_restaurant",
    )


class GroupRestaurantRating(Base):
    """Model for storing individual ratings for group restaurants."""

    __tablename__ = "group_restaurant_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("group_restaurants.id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    group_restaurant: Mapped["GroupRestaurant"] = relationship(
        "GroupRestaurant",
        back_populates="ratings",
        foreign_keys=[group_restaurant_id],  # Specify the foreign key column
    )
