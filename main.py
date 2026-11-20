import requests_cache
import data_manager
import flight_search
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from pprint import pprint
from notification_manager import NotificationManager
#=============== Conserve Requests ===============#
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after = {
        'https://api.sheety.co/af4534fb2a8fd640f693bd23859714aa/flightDeals/prices':requests_cache.DO_NOT_CACHE,
        "https://serpapi.com/search?engine=google_flights":3600,
    }
)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=30*6)
#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
#================ Talk to Shetty ===============#
DataManager = data_manager.DataManager()
sheet_data = DataManager.get_data()
FlightSearch = flight_search.FlightSearch()
# ==================== Retrieve your customer emails ====================

customer_data = DataManager.get_customer_emails()
# Verify the name of your email column in your sheet. Yours may be different from mine
customer_email_list = [row["qualSeuEmail?"] for row in customer_data]
print(customer_email_list)
# print(f"Your email list includes {customer_email_list}")

#=============== Set the Dates ===============#
for destination in sheet_data:
    #=============== Some Variables ==============#
    print(destination)
    Origin_Id = "MCZ"
    Arrival_Id = destination.get("iataCode")
    Row_Id = destination.get("id")
    current_date = tomorrow
    #================ Search up The Flight ================#

    departure_date = current_date.strftime('%Y-%m-%d')
    return_date = (current_date + timedelta(days=7)).strftime("%Y-%m-%d")#data exemplo, de retorno após 7 dias

    FlightSearchResults = FlightSearch.check_flights(origin_city_code=Origin_Id, destination_city_code=Arrival_Id,
                        from_time=departure_date, to_time=return_date)
    #================= Show The Cheapest Flight =================#
    cheapest_flight = find_cheapest_flight(data=FlightSearchResults, return_date=return_date)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        FlightSearchResults = FlightSearch.check_flights(origin_city_code=Origin_Id, destination_city_code=Arrival_Id,
                                                         from_time=departure_date, to_time=return_date, is_direct=False)
        cheapest_flight = find_cheapest_flight(data=FlightSearchResults, return_date=return_date)

    # ================= Show The Cheapest Flight =================#
    pprint(f"{destination.get('city')}:{cheapest_flight.price}")
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination.get("lowestPrice"):
        pprint(f"Lower price flight found to {destination.get('city')}!")
        DataManager.update_cheapest_price(new_price=cheapest_flight.price, row_id=Row_Id)
        notification_manager = NotificationManager(price=cheapest_flight.price,
                                                   origin_airport=Origin_Id,
                                                   destination_airport=destination["city"],
                                                   outbound_date=departure_date
                                                   , inbound_date=return_date,
                                                   number_of_stops=cheapest_flight.number_of_stops,)
        for user_email in customer_email_list:
            notification_manager.send_email(user_email=user_email)
