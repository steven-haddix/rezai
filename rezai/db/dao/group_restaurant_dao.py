from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rezai.db.dependencies import get_db_session
from rezai.db.models.group_restaurant_model import (
    GroupRestaurant,
    GroupRestaurantRating,
)


class GroupRestaurantDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_group_restaurant(self, group_restaurant: GroupRestaurant) -> None:
        self.session.add(group_restaurant)

    async def get_group_restaurant_by_id(
        self,
        group_restaurant_id: int,
    ) -> Optional[GroupRestaurant]:
        result = await self.session.execute(
            select(GroupRestaurant).where(GroupRestaurant.id == group_restaurant_id),
        )
        return result.scalars().first()

    async def get_group_restaurants_by_group_id(
        self,
        group_id: int,
    ) -> List[GroupRestaurant]:
        result = await self.session.execute(
            select(GroupRestaurant).where(GroupRestaurant.group_id == group_id),
        )
        return list(result.scalars().fetchall())

    async def get_group_restaurants_by_restaurant_id(
        self,
        restaurant_id: int,
    ) -> List[GroupRestaurant]:
        result = await self.session.execute(
            select(GroupRestaurant).where(
                GroupRestaurant.restaurant_id == restaurant_id,
            ),
        )
        return list(result.scalars().fetchall())

    async def update_group_restaurant(self, group_restaurant: GroupRestaurant) -> None:
        self.session.add(group_restaurant)

    async def delete_group_restaurant(self, group_restaurant: GroupRestaurant) -> None:
        await self.session.delete(group_restaurant)


class GroupRestaurantRatingDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_group_restaurant_rating(
        self,
        group_restaurant_rating: GroupRestaurantRating,
    ) -> None:
        self.session.add(group_restaurant_rating)

    async def get_group_restaurant_ratings_by_group_id(
        self,
        group_restaurant_id: int,
    ) -> List[GroupRestaurantRating]:
        result = await self.session.execute(
            select(GroupRestaurantRating).where(
                GroupRestaurantRating.group_restaurant_id == group_restaurant_id,
            ),
        )
        return list(result.scalars().fetchall())

    async def get_group_restaurant_ratings_by_user_id(
        self,
        user_id: int,
    ) -> List[GroupRestaurantRating]:
        result = await self.session.execute(
            select(GroupRestaurantRating).where(
                GroupRestaurantRating.user_id == user_id,
            ),
        )
        return list(result.scalars().fetchall())

    async def update_group_restaurant_rating(
        self,
        group_restaurant_rating: GroupRestaurantRating,
    ) -> None:
        self.session.add(group_restaurant_rating)

    async def delete_group_restaurant_rating(
        self,
        group_restaurant_rating: GroupRestaurantRating,
    ) -> None:
        await self.session.delete(group_restaurant_rating)
