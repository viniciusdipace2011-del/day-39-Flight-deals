import requests_cache
from requests_cache import CachedSession, DO_NOT_CACHE, NEVER_EXPIRE
import data_manager
import flight_search
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from pprint import pprint
from notification_manager import NotificationManager
#=============== Conserve Requests ===============#

requests_cache.install_cache(
    expire_after=3600,

)
urls_expire_after = {
    'https://api.sheety.co/af4534fb2a8fd640f693bd23859714aa/flightDeals/prices': DO_NOT_CACHE,
    "https://serpapi.com/search?engine=google_flights":NEVER_EXPIRE,
}
session = CachedSession(urls_expire_after=urls_expire_after)

#=============== Set the Dates ===============#

tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')
six_month_from_today = datetime.now() + timedelta(days=30*6)
six_month_from_today = six_month_from_today.strftime('%Y-%m-%d')


#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
#================ Talk to Shetty ===============#
DataManager = data_manager.DataManager()
sheet_data = DataManager.get_data()
for city in sheet_data:
    #=============== Some Variables ==============#
    print(city)
    Origin_Id = "MCZ"
    Arrival_Id = city.get("iataCode")
    Row_Id = city.get("id")
    #================ Search up The Flight ================#
    FlightSearch = flight_search.FlightSearch()
    FlightSearchResults = FlightSearch.check_flights(origin_city_code=Origin_Id, destination_city_code=Arrival_Id,
                         from_time=tomorrow, to_time=six_month_from_today)
    print(FlightSearchResults)
    #================= Show The Cheapest Flight =================#
    cheapest_flight = find_cheapest_flight(data=FlightSearchResults, return_date=six_month_from_today)
    pprint(f"{city.get('city')}: GBP {cheapest_flight.price}")


    if cheapest_flight.price != "N/A" and cheapest_flight.price < city.get("lowestPrice"):
        pprint(f"Lower price flight found to {city.get('city')}!")
        DataManager.update_cheapest_price(FlightSearchResults, Row_Id)
        notification_manager = NotificationManager(price=city.get("price"),
                departure_airport_iata_code=Origin_Id,
                arrival_airport_iata_code=Arrival_Id,outbound_date=FlightSearchResults.get("outbound_date")
                                                   ,inbound_date=FlightSearchResults.get("inbound_date"))
        notification_manager.send_message()