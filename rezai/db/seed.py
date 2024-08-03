import csv
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from rezai.db.models.restaurant_model import Restaurant


async def seed_restaurants_from_tsv(session: AsyncSession, tsv_file: str) -> None:
    """
    Seed the database with restaurants from a TSV file.

    :param session: The database session.
    :param tsv_file: The TSV file to read from.
    """
    file_path = Path(__file__).parent.parent.parent / "data" / tsv_file
    print(file_path)
    with open(file_path, "r") as file:
        reader = csv.DictReader(file, delimiter="\t")
        restaurants = []
        for row in reader:
            restaurant = Restaurant(
                title=row["Restaurant"],
                type=row["Cusine Style"],
                category=row["Cusine Style"],
            )
            restaurants.append(restaurant)
        session.add_all(restaurants)
        await session.commit()


async def seed_database(session: AsyncSession) -> None:
    """
    Seed the database with data from the TSV files.

    :param session: The database session.
    """
    await seed_restaurants_from_tsv(session, "restaurants.tsv")
