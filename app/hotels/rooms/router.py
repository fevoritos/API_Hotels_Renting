from datetime import date, datetime, timedelta

from fastapi import Query
from app.hotels.rooms.dao import RoomDAO
from app.hotels.router import router

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id:int,
    date_from:date = Query(..., description=f"Например, {datetime.now().date()}"), 
    date_to:date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}"),
    ):
    return await RoomDAO.get_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)