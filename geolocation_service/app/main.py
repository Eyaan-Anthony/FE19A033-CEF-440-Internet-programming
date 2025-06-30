#entry point of the Fast Api
from app.api import glc_routes
from fastapi import FastAPI

app = FastAPI()

#include routers
app.include_router(glc_routes.router, prefix="/geolocation", tags=["geolocation"])
#creation of a route to handle all authentifications, so this enables all the endpoints defined in the geolocation services,