from geopy.distance import geodesic

def check_location(
    target_lat: float,
    target_long: float,
    student_lat: float,
    student_long: float,
    radius_meters: float = 10
) -> tuple[bool, float]:
    """Returns True if student is within radius, else False. Also returns distance."""
    target_coords = (target_lat, target_long)
    student_coords = (student_lat, student_long)

    distance = geodesic(target_coords, student_coords).meters
    within_radius = distance <= radius_meters

    return within_radius, distance