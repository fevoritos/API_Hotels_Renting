from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependenies import get_current_user
from app.users.models import Users
from typing import List

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
    room_id:int, 
    date_from:date = Query(..., description=f"Например, {datetime.now().date()}"), 
    date_to:date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}"),
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to
    )
    
    if not booking:
        raise RoomCannotBeBooked
    
    # booking_dict = SBooking.model_validate(booking).model_dump()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # return booking_dict
    return booking
    

@router.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id:int,
    user: Users = Depends(get_current_user),
):
    return await BookingDAO.delete(user_id=user.id, id=booking_id)