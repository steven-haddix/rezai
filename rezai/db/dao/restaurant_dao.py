from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rezai.db.dependencies import get_db_session
from rezai.db.models.restaurant_model import Restaurant


class RestaurantDAO:
    """
    Data access object for the restaurant model.

    This class provides methods to interact with the restaurant model.
    """

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_restaurant(self, restaurant: Restaurant) -> None:
        """
        Create a new restaurant in the database.

        :param restaurant: The restaurant to create.
        """
        self.session.add(restaurant)

    async def get_all_restaurants(self, limit: int, offset: int) -> List[Restaurant]:
        """
        Get all restaurants from the database.

        :param limit: The maximum number of restaurants to return.
        :param offset: The number of restaurants to skip.

        :return: A list of restaurants.
        """
        raw_restaurants = await self.session.execute(
            select(Restaurant).limit(limit).offset(offset),
        )
        return list(raw_restaurants.scalars().fetchall())

    async def filter(
        self,
        title: Optional[str] = None,
        type: Optional[str] = None,  # noqa: WPS125
        category: Optional[str] = None,
        address: Optional[str] = None,
        min_rating: Optional[int] = None,
        max_reviews: Optional[int] = None,
        unclaimed: Optional[bool] = None,
    ) -> List[Restaurant]:
        """
        Filter restaurants based on the given criteria.

        :param title: The title of the restaurant.
        :param type: The type of the restaurant.
        :param category: The category of the restaurant.
        :param address: The address of the restaurant.
        :param min_rating: The minimum rating of the restaurant.
        :param max_reviews: The maximum number of reviews of the restaurant.
        :param unclaimed: Whether the restaurant is unclaimed.
        :return: A list of restaurants that match the criteria.
        """
        query = select(Restaurant)
        if title:
            query = query.where(Restaurant.title == title)
        if type:
            query = query.where(Restaurant.type == type)
        if category:
            query = query.where(Restaurant.category == category)
        if address:
            query = query.where(Restaurant.address.ilike(f"%{address}%"))
        if min_rating:
            query = query.where(Restaurant.rating >= min_rating)
        if max_reviews:
            query = query.where(Restaurant.reviews <= max_reviews)
        if unclaimed is not None:
            query = query.where(Restaurant.unclaimed == unclaimed)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
