"""
Interaction with BusinessFrance's API
"""
import sqlite3
import requests
from utils import get_payload, Filters

API_URL_BASE = "https://civiweb-api-prd.azurewebsites.net/api/Offers/"
API_URL_OFFER = API_URL_BASE + "search"
API_URL_GEOGRAPHIC_ZONES = API_URL_BASE + "repository/geographic-zones"
API_URL_COUNTRIES = API_URL_GEOGRAPHIC_ZONES + "/countries"



def fetch_offers(filters:Filters = None)-> dict:
    print("filters : "+ str(filters))
    print("payload : "+ str(get_payload(filters=filters)))
    response = requests.post(url=API_URL_OFFER, json=get_payload(filters=filters))
    print("res" + str(response.json()))
    response.raise_for_status()
    return response.json()

def set_filters(user_id: int, query: str = None, location: str = None, last_alerted_at: str = None) -> None:
    print("Setting filters")
    with sqlite3.connect('viebot.db') as conn:
        conn.execute('''
        INSERT INTO filters (user_id, query, location, last_alerted_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET query = excluded.query, location = excluded.location, last_alerted_at = excluded.last_alerted_at
        ''', (user_id, query, location, last_alerted_at))
        conn.commit()
        print("Filters updated!")

def get_filters(user_id: int) -> Filters:
    with sqlite3.connect('viebot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT query, location FROM filters WHERE user_id = ?', (user_id,))
        result = c.fetchone()
    
    if result:
        query, location = result
        return {"query": query, "location": location}
    return None

def populate_geographic_zones():
    try:
        response = requests.get(url=API_URL_GEOGRAPHIC_ZONES)
        response.raise_for_status()
        res = response.json()
    except requests.RequestException as e:
        print(f"Error raised when request to API is sent : {e}")
        return
    except ValueError:
        print("Error getting json() from response")
        return

    with sqlite3.connect('viebot.db') as conn:
        c = conn.cursor()
        for geographic_zone in res.get("result", []):
            zone_id = geographic_zone.get("geographicZoneId")
            zone_label = geographic_zone.get("geographicZoneLabel")
            if zone_id is None or zone_label is None:
                print(f"Missing keys in response : {geographic_zone}")
                continue
            c.execute('''
                INSERT OR IGNORE INTO geo_zones (id, name)
                VALUES(?, ?)
            ''', (zone_id, zone_label))
        conn.commit()
    print(f"{len(res.get('result', []))} geographic zones inserted in DB")

def populate_countries():
    try:
        response = requests.post(url=API_URL_COUNTRIES, json=[])
        response.raise_for_status()
        res = response.json()
    except requests.RequestException as e:
        print(f"Error raised when request to API is sent : {e}")
        return
    except ValueError:
        print("Error getting json() from response")
        return

    inserted_count = 0 
    with sqlite3.connect('viebot.db') as conn:
        c = conn.cursor()
        for country in res:
            country_id = country.get("countryId")
            country_label = country.get("countryName")
            country_geographic_zone_id = country.get("geographicZoneId")
            if country_id is None or country_label is None or country_geographic_zone_id is None:
                print(f"Missing keys in response : {country}")
                continue
            c.execute('''
                INSERT OR IGNORE INTO countries (id, name, geo_zone_id)
                VALUES(?, ?, ?)
            ''', (country_id, country_label, country_geographic_zone_id))
            inserted_count += 1
        conn.commit()
    print(f"{inserted_count} countries inserted in DB")
