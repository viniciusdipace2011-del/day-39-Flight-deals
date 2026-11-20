import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
class FlightSearch:
    def __init__(self):
        #This class is responsible for talking to the Flight Search API
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.six_month_from_today = datetime.today() + timedelta(days=30 * 6)
        self.Flight_API_Endpoint = "https://serpapi.com/search?engine=google_flights"
        self.Flight_API_Key = os.getenv('SERPAPI_API_KEY')
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": "1",
            "adults": "1",
            "currency": "BRL",
            "api_key": self.Flight_API_Key,
        }
        if is_direct:
            params["stops"] = "1"

        response = requests.get(self.Flight_API_Endpoint, params=params)
        if response.status_code != 200:
            print(response.status_code, response.text)
            return None
        else:
            data = response.json()
            if "error" in data:
                print(f"Flight search returned {data['error']}")
                return None
            else:
                return data
