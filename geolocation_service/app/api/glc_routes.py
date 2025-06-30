from fastapi import APIRouter, HTTPException
from service.glc_service import check_location
from models.glc_model import LocationCheckResponse, LocationCheckRequest

router = APIRouter()

@router.post("/check-location", response_model=LocationCheckResponse)
async def check_location_route(data: LocationCheckRequest):
    try:
        within_radius, distance = check_location(
            data.target_lat,
            data.target_long,
            data.student_lat,
            data.student_long,
            data.radius_meters
        )
        return LocationCheckResponse(
            within_radius=within_radius,
            distance_meters=distance
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
