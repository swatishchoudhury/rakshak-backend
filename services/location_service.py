from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List, Dict

geolocator = Nominatim(user_agent="sos_app")


class LocationService:
    @staticmethod
    def get_district(coordinates: str) -> str:
        try:
            lat, lon = map(float, coordinates.split(","))
            location = geolocator.reverse(f"{lat}, {lon}")
            address = location.raw["address"]
            return address.get(
                "state_district", address.get("county", address.get("city", "Unknown"))
            )
        except Exception as e:
            print(f"An error occurred while getting district: {str(e)}")
            return "Unknown"

    @staticmethod
    def sort_responders_by_distance(
        responders: List[Dict], sos_coordinates: str
    ) -> List[Dict]:
        sos_point = tuple(map(float, sos_coordinates.split(",")))
        for responder in responders:
            responder_point = tuple(
                map(float, responder.get("coordinates", "0,0").split(","))
            )
            responder["distance"] = geodesic(sos_point, responder_point).kilometers
        return sorted(responders, key=lambda x: x["distance"])
