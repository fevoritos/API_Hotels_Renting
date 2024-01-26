from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)


class HotelSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date, 
        date_to: date,
        has_spa: bool = Query(default=None),
        stars: int = Query(ge=1, le=5, default=None)     
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars
        
        


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels", response_model=list[SHotel])
def get_hotels(
    search_args: HotelSearchArgs = Depends()
    # location: str,
    # date_from: date, 
    # date_to: date,
    # has_spa: bool = Query(default=None),
    # stars: int = Query(ge=1, le=5, default=None)
):
    hotels = [
        {
            "address": "Ул. Пушкина, 3, Санкт-Петербург",
            "name": "Omega Hotel",
            "stars": 5,
        }
    ]

    return search_args


class SBookig(BaseModel):
    room_id: int
    date_from: date 
    date_to: date


@app.post("/booking")
def add_booking(booking: SBookig):
    pass