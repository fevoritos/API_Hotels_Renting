from sqlalchemy import select
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker


class HotelDAO(BaseDAO):
    model = Hotels

    # @classmethod
    # async def find_all(cls):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns)
    #         result = await session.execute(query)
    #         return result.mappings().all()