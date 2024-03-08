from app.bookings.models import Bookings
from app.database import async_session_maker
from sqlalchemy import and_, func, select, insert

from app.hotels.rooms.models import Rooms

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
 
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def rooms_left(cls, date_from, date_to):
        booked_rooms = select(Bookings).where(
            and_( 
                (Bookings.date_from <= date_to),
                (Bookings.date_to >= date_from)
            )
        ).cte()

        subq = select((func.greatest(Rooms.quantity - func.count(booked_rooms.c.room_id), 0)).label("rooms_left"), Rooms.id
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id,  isouter=True
                ).group_by(
                    Rooms.id, Rooms.quantity, booked_rooms.c.room_id).cte()
        
        return  subq