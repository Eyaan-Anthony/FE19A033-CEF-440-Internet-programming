#entry point of the Fast Api
from app.api import auth_routes
from fastapi import FastAPI

app = FastAPI()

#include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
#creation of a route to handle all authentifications, so this enables all the endpoints defined in auth_routes,
#to be used effectively within authentification