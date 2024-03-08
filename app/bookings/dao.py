from datetime import date
from app.dao.base import BaseDAO
from app.database import async_session_maker

from sqlalchemy import delete, insert, select, func, and_, or_
from app.bookings.models import Bookings
from app.exceptions import CanNotAddBooking, CanNotFindBooking
from app.hotels.rooms.models import Rooms

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_bookings(
        cls,
        user_id: int,
    ):
        async with async_session_maker() as session:
            f_bookings = select(
                Bookings.room_id, Bookings.user_id, 
                Bookings.date_from, Bookings.date_to,
                Bookings.price, Bookings.total_cost, Bookings.total_days,
                Rooms.image_id, Rooms.name, Rooms.description, Rooms.services
                ).join(Bookings, Bookings.room_id == Rooms.id).where(Bookings.user_id==user_id)
            f_bookings = await session.execute(f_bookings)
            f_bookings = f_bookings.mappings().all()
            return f_bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        if (date_to-date_from).days <= 0:
            raise CanNotAddBooking
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id==room_id,
                    and_( 
                        (Bookings.date_from <= date_to),
                        (Bookings.date_to >= date_from)
                    )
                )
            ).cte()

            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """

            get_rooms_left = select(
                Rooms.quantity - func.count(booked_rooms.c.room_id)
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id,  isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
            
            rooms_left = await session.execute(get_rooms_left)
            rooms_left:int = rooms_left.scalar()
            
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_bookings = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_bookings)
                await session.commit()
                return new_booking.scalar()

            else:
                return None
    
    @classmethod
    async def delete(
        cls,
        user_id: int,
        id: int
    ):
        async with async_session_maker() as session:
            find_booking = select(Bookings).where(
                and_(
                    Bookings.user_id == user_id,
                    Bookings.id == id
                )
            )
            find_booking = await session.execute(find_booking)
            find_booking = find_booking.scalar_one_or_none()
            if find_booking == None:
                raise CanNotFindBooking

        async with async_session_maker() as session:
            delete_booking = delete(Bookings).where(
                and_(
                    Bookings.user_id == user_id,
                    Bookings.id == id
                )
            )
            delete_booking = await session.execute(delete_booking)
            await session.commit()

