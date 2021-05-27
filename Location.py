class Location:
    count_id = 0

    def __init__(self, neighbourhood, address, area, availability):
        Location.count_id += 1
        self.__location_id = Location.count_id
        self.__neighbourhood = neighbourhood
        self.__address = address
        self.__area = area
        self.__availability = availability

    def get_location_id(self):
        return self.__location_id

    def get_neighbourhood(self):
        return self.__neighbourhood

    def get_address(self):
        return self.__address

    def get_area(self):
        return self.__area

    def get_availability(self):
        return self.__availability

    def set_location_id(self, location_id):
        self.__location_id = location_id

    def set_neighbourhood(self, neighbourhood):
        self.__neighbourhood = neighbourhood

    def set_address(self, address):
        self.__address = address

    def set_area(self, area):
        self.__area = area

    def set_availability(self, availability):
        self.__availability = availability
