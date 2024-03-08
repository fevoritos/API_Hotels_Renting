from datetime import date
from app.dao.base import BaseDAO
from app.exceptions import CanNotAddBooking
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from sqlalchemy import delete, insert, select, func, and_, or_
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
        if (date_to-date_from).days <= 0:
            raise CanNotAddBooking
        
        async with async_session_maker() as session:
            delta_days = (date_to-date_from).days
            subq = await RoomDAO.rooms_left(date_to=date_to,date_from=date_from)

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