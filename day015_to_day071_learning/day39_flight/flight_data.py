class FlightData:
    """This class is responsible for structuring the flight data."""

    def __init__(self, data):
        self.data = data
        self.sms_data = []

    def check_dup(self, city, on, until):
        """ This function checks if there already is flight for same dates. """
        for flight in self.sms_data:
            if flight["destination"] == city:
                if flight["on"][:10] == on[:10] and flight["until"][:10] == until[:10]:
                    return False
        return True

    def process_data_to_sms(self):
        """ This function processes found flight data to valid offers to pass it to sms."""
        data = {key: value for (key, value) in self.data.items() if value != []}
        for key in data:
            for date in data[key]:
                for offer in date:

                    on = offer["itineraries"][0]["segments"][0]["departure"]["at"]
                    until = offer["itineraries"][1]["segments"][0]["departure"]["at"]

                    if self.check_dup(key, on, until):

                        self.sms_data.append({
                            "destination": key,
                            "price": offer["price"]["currency"] + offer["price"]["total"],
                            "from": offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                            "to": offer["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
                            "on": on,
                            "until": until
                        })

        print(self.sms_data)
        # text = f"Low price alert! Only {}{} to fly from {} to {}, on {} until {}."