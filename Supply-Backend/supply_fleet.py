# Class: Fleet
# Concern: Supply

from supply_vehicle import Vehicle
import math

class Fleet:

    def __init__ (self, fleet_name, fleet_region, fleet_vehicles=[], warehouses=[]):
        self._fleet_name = fleet_name
        self._fleet_region = fleet_region
        self._fleet_vehicles = fleet_vehicles
        self._warehouses = warehouses

    # getter method for fleet name
    @property
    def fleet_name(self):
        return self._fleet_name
    
    # setter method for fleet name
    @fleet_name.setter
    def fleet_name(self, value):
        self._fleet_name = value

    # getter method for fleet region
    @property
    def fleet_region(self):
        return self._fleet_region
    
    # setter method for fleet region
    @fleet_region.setter
    def fleet_region(self, value):
        self._fleet_region = value
        
    # getter method for fleet size
    @property
    def fleet_size(self):
        return len(self.fleet_vehicles)
    
    # getter method for fleet vehicles
    @property
    def fleet_vehicles(self):
        return self._fleet_vehicles
    
    # insert a vehicle into the fleet with vin
    def fleet_insert_vehicle(self, vehicle):
        self.fleet_vehicles.append(vehicle.vin)
        print ("Vehicle", vehicle.vin, "inserted into fleet!")
        
    # remove a vehicle from the fleet using vin
    def fleet_remove_vehicle(self, vehicle):
        self.fleet_vehicles.remove(vehicle.vin)
        print ("Vehicle", vehicle.vin, "inserted into fleet!")
        
    # getter method for all values of fleet
    @property
    def dictionary(self):
        fleet_dictionary = {
            "fleet_name": self.fleet_name,
            "fleet_region": self.fleet_region,
            "fleet_size": self.fleet_size,
            "fleet_vehicles": self.fleet_vehicles,
            "warehouses": self.warehouses
        }
        return fleet_dictionary
    
    # return the closest warehouse to the given position
    def get_closest_warehouse (self, position):
        if len(self.warehouses) == 0:
            return None
        closest_warehouse = self.warehouses[0]
        if len(self.warehouses) != 1:
            closest_distance = self.calculate_distance (closest_warehouse["coordinates"])
            for index in range (1, len (self.warehouses)):
                warehouse_position = self.warehouses[index]["coordinates"]
                distance = self.calculate_distance (position, warehouse_position)
                if (closest_distance > distance):
                    closest_warehouse = self.warehouses[index]
        return closest_warehouse
        
    # https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
    # output the distance between two coordinates in kilometers
    def calculate_distance (self, latlong1, latlong2):
        R = 6373.0 # radius of the Earth in km
        
        # coordinates
        lat1 = math.radians(latlong1[0])
        lon1 = math.radians(latlong1[1])
        lat2 = math.radians(latlong2[0])
        lon2 = math.radians(latlong2[1])
        
        # change in coordinates
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return distance
    
####################### testing methods ####################################
#new_fleet = FleetManager("prison", "bus")

#print(new_fleet.get_fleet_name(),new_fleet.get_fleet_vehicle())
#############################################################################