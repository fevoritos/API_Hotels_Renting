from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
async def get_hotels(
    location:str,
    date_from:date = Query(..., description=f"Например, {datetime.now().date()}"), 
    date_to:date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}"),
):
    return await HotelDAO.get_hotels(
        location=location, 
        date_from=date_from,
        date_to=date_to)

@router.get("/id/{hotel_id}") 
async def get_hotel_info(hotel_id:int):
    return await HotelDAO.find_all(id = hotel_id)