import sqlite3
from typing import TypedDict, Optional, Union

class BusinessFranceOffersPayload(TypedDict):
    limit: int
    skip: int
    query: str
    activitySectorId: list[int]
    missionsTypesIds: list[int]
    missionsDurations: list[int]
    gerographicZones: list[int]
    countriesIds: list[int]
    studiesLevelId: list[int]
    companiesSizes: list[int]
    specializationsIds: list[int]
    entreprisesIds: list[int]
    missionStartDate:Optional[str]

class Filters(TypedDict):
    query: str
    location: str

def get_payload(limit: int = 10, filters: Filters = None) -> BusinessFranceOffersPayload:
    locations_data = None

    if filters:
        location = filters.get("location")
        if location:
            locations_data = map_location(location) or []

    
    return {
        "limit":limit,
        "skip":0,
        "query": filters.get("query") if filters else "",
        "activitySectorId":[],
        "missionsTypesIds":[],
        "missionsDurations":[],
        "gerographicZones":[
            str(location_data["id"]) for location_data in locations_data if location_data["type"] == "geo_zone"
        ] if locations_data else [],
        "countriesIds":[
            str(location_data["id"]) for location_data in locations_data if location_data["type"] == "country"
        ] if locations_data else [],
        "studiesLevelId":[],
        "companiesSizes":[],
        "specializationsIds":[],
        "entreprisesIds":[],
        "missionStartDate":None
    }

def map_location(location: str) -> Union[dict, None]:
    location = location.strip().lower()
    with sqlite3.connect('viebot.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT id, name FROM geo_zones WHERE LOWER(name) LIKE ?
        ''', (f"%{location}%",))
        geo_zones = c.fetchall()
        if geo_zones:
            return [{"type": "geo_zone", "id": zone[0], "name": zone[1]} for zone in geo_zones]

        c.execute('''
                SELECT id, name FROM countries WHERE LOWER(name) LIKE ?
            ''', (f"%{location}%",))
        countries = c.fetchall()

        if countries:
            return [{"type": "country", "id": country[0], "name": country[1]} for country in countries]
        
        return []
 

def format_offer(offer: dict) -> str:
    return f"{offer['missionTitle']} - {offer['organizationName']} ({offer['cityName']})"


def build_filters(ctx, *args) -> Union[Filters, None]:
    if not args:
        return None

    input_str = " ".join(args).strip()
    if not input_str:
        return None

    if " à " in input_str:
        query, location = input_str.split(" à ", 1)
    else:
        # If separator 'à' not in args, then location is None
        query, location = input_str, None
    return  Filters(query=query.strip(), location=location.strip() if location else None)