#entry point of the Fast Api
from app.api import fcr_routes
from fastapi import FastAPI

app = FastAPI()

#include routers
app.include_router(fcr_routes.router, prefix="/fcr", tags=["fcr"])
#creation of a route to handle all authentifications, so this enables all the endpoints defined in the facial
# recognition service,