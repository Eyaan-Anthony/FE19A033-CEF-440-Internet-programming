#entry point of the Fast Api
from app.api import class_session_routes
from fastapi import FastAPI

app = FastAPI()

#include routers
app.include_router(class_session_routes.router, prefix="/classs-session", tags=["Class Sessions"])
#creation of a route to handle all authentifications, so this enables all the endpoints defined in 
# class_session routes,
