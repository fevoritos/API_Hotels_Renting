from datetime import date
from sqlalchemy import select, func, and_
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels(
        cls,
        location:str,
        date_from:date, 
        date_to:date,
    ):
        location = location.capitalize()

        async with async_session_maker() as session:
            row = await HotelDAO.rooms_left(date_from=date_from, date_to=date_to)
            rooms_left = select(
                row.c.rooms_left, row.c.id, Rooms.hotel_id
                ).join(Rooms, Rooms.id==row.c.id).cte()
            
            # rooms_left = await session.execute(rooms_left)
            # return rooms_left.mappings().all()

            query = select(
                Hotels.id, Hotels.name, Hotels.location, 
                Hotels.services, Hotels.rooms_quantity, Hotels.image_id,
                (func.sum(rooms_left.c.rooms_left)).label("rooms_left")
                ).select_from(Hotels).join(
                    rooms_left, Hotels.id == rooms_left.c.hotel_id, isouter=True
                ).group_by(
                  Hotels.id  
                ).where(       
                    Hotels.location.like(f"%{location}%"),     
                ).cte()
            
            qq = select(query).where(query.c.rooms_left > 0)
            
            result = await session.execute(qq)
            return result.mappings().all()