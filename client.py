"""
Interaction with BusinessFrance's API
"""
import requests
from utils import get_payload

API_URL = "https://civiweb-api-prd.azurewebsites.net/api/Offers/search"

def fetch_offers()-> dict:
    response = requests.post(url=API_URL, json=get_payload(limit=10))
    print("res" + str(response.json()))
    response.raise_for_status()
    return response.json()