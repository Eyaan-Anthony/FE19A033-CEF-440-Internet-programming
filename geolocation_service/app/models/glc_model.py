from pydantic import BaseModel, Field
from typing import Literal

class LocationCheckRequest(BaseModel):
    target_lat: float = Field(..., description="Latitude of the class location")
    target_long: float = Field(..., description="Longitude of the class location")
    student_lat: float = Field(..., description="Latitude of the student location")
    student_long: float = Field(..., description="Longitude of the student location")
    radius_meters: float = Field(10, description="Radius to check within, in meters")

class LocationCheckResponse(BaseModel):
    within_radius: bool
    distance_meters: float