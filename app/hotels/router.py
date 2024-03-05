from fastapi import APIRouter

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/id/{hotel_id}") 
async def get_hotel_info(hotel_id:int):
    return await HotelDAO.find_all(id = hotel_id)