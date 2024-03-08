from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as router_pages

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_rooms)

app.include_router(router_pages)

