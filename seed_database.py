import asyncio

from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from rezai.db.seed import seed_database
from rezai.settings import settings


async def main() -> None:
    """Seed the database with data from the TSV files."""
    engine = create_async_engine(str(settings.db_url), echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            await seed_database(session)
            await session.commit()
            logger.info("Database seeding completed successfully.")
        except Exception as ex:
            await session.rollback()
            logger.info(f"Error occurred during database seeding: {str(ex)}")


if __name__ == "__main__":
    asyncio.run(main())
