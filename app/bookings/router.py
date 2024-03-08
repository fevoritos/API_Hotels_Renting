from datetime import date
from fastapi import APIRouter, Depends, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependenies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)
):
    return await BookingDAO.get_bookings(user_id=user.id)


@router.post("")
async def add_booking(
    room_id:int, date_from:date, date_to:date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    
@router.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id:int,
    user: Users = Depends(get_current_user),
):
    return await BookingDAO.delete(user_id=user.id, id=booking_id)