# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

data_manager = DataManager()
sheet_data = data_manager.get_flights_data()

flight_search = FlightSearch(sheet_data)
flights_data = flight_search.find_flights()

flight_data = FlightData(flights_data)
flight_data.process_data_to_sms()


# print(flight_search.sheet_data)


