from datetime import date
from fastapi import APIRouter

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
async def get_hotels(
    location:str,
    date_from:date, 
    date_to:date,
):
    return await HotelDAO.get_hotels(
        location=location, 
        date_from=date_from,
        date_to=date_to)

@router.get("/id/{hotel_id}") 
async def get_hotel_info(hotel_id:int):
    return await HotelDAO.find_all(id = hotel_id)