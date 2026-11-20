import requests
import os
from dotenv import load_dotenv
load_dotenv()
class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.Shetty_API_Endpoint = "https://api.sheety.co/af4534fb2a8fd640f693bd23859714aa/flightDeals/prices"
        self.headers = {
            "Authorization": os.getenv('SHETTY_AUTH_TOKEN')
        }
    def get_data(self):
        response = requests.get(self.Shetty_API_Endpoint, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["prices"]
    def update_cheapest_price(self, row_id, new_price):
        print("This was run")
        new_data = {
                 "price":{
                     "lowest Price":new_price
                 }
        }
        response = requests.put(f'{self.Shetty_API_Endpoint}/{row_id}', headers=self.headers, json=new_data)
        response.raise_for_status()
        print(response.json())
