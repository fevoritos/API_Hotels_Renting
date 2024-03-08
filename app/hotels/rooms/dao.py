from datetime import date
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from sqlalchemy import delete, insert, select, func, and_, or_, text
from app.database import async_session_maker


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms(
        cls,
        hotel_id:int,
        date_from:date, 
        date_to:date
    ):
               
        async with async_session_maker() as session:
            delta_days = (date_to-date_from).days

            booked_rooms = select(Bookings).where(
                and_( 
                    (Bookings.date_from <= date_to),
                    (Bookings.date_to >= date_from)
                )
            ).cte()

            subq = select((Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"), Rooms.id
                    ).select_from(Rooms).join(
                        booked_rooms, booked_rooms.c.room_id == Rooms.id,  isouter=True
                    ).group_by(
                        Rooms.id, Rooms.quantity, booked_rooms.c.room_id).cte()
            
            g_rooms = select(
                Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, 
                Rooms.services, Rooms.price, Rooms.quantity, Rooms.image_id, 
                (Rooms.price * delta_days).label("total_cost"), subq.c.rooms_left
                ).select_from(Rooms).join(
                   subq, Rooms.id == subq.c.id, isouter=True
                ).where(
                    Rooms.hotel_id == hotel_id
                ) 
                     
            g_rooms = await session.execute(g_rooms)
            return g_rooms.mappings().all()