from typing import TypedDict, Optional

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

def get_payload(limit: int) -> BusinessFranceOffersPayload:
    return {
        "limit":limit,
        "skip":0,
        "query":"",
        "activitySectorId":[],
        "missionsTypesIds":[],
        "missionsDurations":[],
        "gerographicZones":[],
        "countriesIds":[],
        "studiesLevelId":[],
        "companiesSizes":[],
        "specializationsIds":[],
        "entreprisesIds":[0],
        "missionStartDate":None
    }

def format_offer(offer: dict) -> str:
    return f"{offer['missionTitle']} - {offer['organizationName']} ({offer['cityName']})"
