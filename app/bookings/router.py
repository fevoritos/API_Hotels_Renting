from fastapi import APIRouter, Depends, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependenies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

# @router.post("")
# async def add_booking(
#     user: Users = Depends(get_current_user),
# ):
#     return await BookingDAO.find_all(user_id=user.id)