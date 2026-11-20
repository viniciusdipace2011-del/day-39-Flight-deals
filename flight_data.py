class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self,price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

def find_cheapest_flight(data, return_date):
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A","N/A")

    all_flights = data.get("best_flights", []) + data.get("other_flights", [])
    valid_flights = [flight for flight in all_flights if flight.get("price") is not None]
    if not valid_flights:
        return FlightData("N/A","N/A","N/A","N/A","N/A")

    first_flight = valid_flights[0]

    lowest_price = first_flight["price"] #this is already a number(no conversion needed)

    origin_airport = first_flight["flights"][0]["departure_airport"]["id"] # Origin airport

    destination_airport = first_flight["flights"][-1]["arrival_airport"]["id"] #Destination airport

    departure_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0] #Departure date

    #Initialize Comparison
    cheapest_flight = FlightData(lowest_price, origin_airport, destination_airport, departure_date, return_date)
    for flight in valid_flights:
        # Exception handling - JSON has data but flight is missing 'price'. Skip.
        try:
            price = flight["price"]
        except KeyError:
            print("--- No price available for flight. ---")
            continue
        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is {lowest_price}")

    return cheapest_flight