import requests
import os
from dotenv import load_dotenv

load_dotenv()
class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.Shetty_Prices_API_Endpoint = "https://api.sheety.co/af4534fb2a8fd640f693bd23859714aa/flightDeals/prices"
        self.Shetty_Users_API_Endpoint = "https://api.sheety.co/af4534fb2a8fd640f693bd23859714aa/flightDeals/users"
        self.headers = {
            "Authorization": os.getenv('SHETTY_AUTH_TOKEN')
        }
        self.customer_data = None
    def get_data(self):
        response = requests.get(self.Shetty_Prices_API_Endpoint, headers=self.headers)
        response.raise_for_status()
        print(response.json())
        data = response.json()
        return data["prices"]
    def update_cheapest_price(self, row_id, new_price):

        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{self.Shetty_Prices_API_Endpoint}/{row_id}",
            json=new_data,
            headers=self.headers
            )
    def get_customer_emails(self):
        response = requests.get(self.Shetty_Users_API_Endpoint, headers=self.headers)
        response.raise_for_status()
        print(response.json())
        data = response.json()
        self.customer_data = data["users"]
        print(self.customer_data)
        return self.customer_data


