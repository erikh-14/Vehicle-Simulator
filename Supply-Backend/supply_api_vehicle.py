from supply_dispatch import Dispatch
from mapping_services import Mapping_Services
from supply_vehicle import Vehicle
from supply_vehicle import Vehicle_Type
from supply_fleet import Fleet
from supply_database_utils import Supply_Database_Utils

import math
import random
import vin_generator

# Vehicle parameters:
    # vin - String - Vehicle Identification Number
    # vehicle_name - String - Name of vehicle
    # vehicle_type - String - Type of the vehicle such as Bus, Van, Truck
    # vehicle_color - String - Color of the vehicle, such as Red, Blue, Green
    # is_available - Bool - Is the vehicle available for service?

def request_vehicle(incoming_dictionary):
    # Grab strings of the incoming dictionary
    vehicle_type = str(incoming_dictionary["vehicle_type"])
    username = str(incoming_dictionary["username"])
    stops = incoming_dictionary["stops"]
    
    print ("Stops: " + str(stops))

    # Creating database utils object to interact with the database
    database_utils = Supply_Database_Utils()

    # Create a Mapping_Services object that will request info from Mapbox.
    mapping_service = Mapping_Services (stops)
    directions = mapping_service.get_directions()

    # Retrieve eta from map services based on stops
    eta = directions.eta
    
    # get the route coordinates
    route = directions.map_route_coordinates

    # create dispatch
    new_dispatch = Dispatch (
        stops,
        route,
        vehicle_type
    )
    
    # insert dispatch into database
    insert_dispatch_result = database_utils.insert_dispatch(new_dispatch)

    # if dispatch inserted into db successfully
    if insert_dispatch_result.acknowledged:
        print ("Inserted dispatch into database successfully!")
        dispatch_from_db = database_utils.get_dispatch_from_id(insert_dispatch_result.inserted_id)
        print (database_utils.get_dispatch_from_id(insert_dispatch_result.inserted_id))
        
        # take all the dictionaries and combine them into one
        python_dictionary = {
            "username": username,
            "start_timestamp": dispatch_from_db["start_timestamp"],
            "vehicle_type": vehicle_type,
            "stops": stops,
            "route": route,
            "eta": eta,
            "dispatch_id": str(insert_dispatch_result.inserted_id)
        }
        
        # assign dispatch to a vehicle
        available_vehicles = database_utils.get_available_vehicles_from_type(vehicle_type)
        selected_vehicle = determine_nearest_vehicle (available_vehicles, route[0])
        if selected_vehicle != None:
            new_dispatch.vehicle_id = selected_vehicle["_id"]
            database_utils.update_dispatch (new_dispatch)
        
        return python_dictionary
        
    else:
        print ("Dispatch could not be inserted database!")
        return None

# Registers a vehicle using a vehicle object
def register_vehicle(vehicle):
    # Creating database utils object to interact with the database
    database_utils = Supply_Database_Utils()

    vehicle_object = vehicle
    insert_result = database_utils.insert_vehicle(vehicle_object)
    
    del database_utils
    if insert_result != None:
        return True
    else:
        return False

# Removes a vehicle from the db using the vin
def remove_vehicle(vin):
    # Creating database utils object to interact with the database
    database_utils = Supply_Database_Utils()

    # Find the vehicle using the vin and delete it
    delete_result = database_utils.delete_vehicle_using_vin (vin)
    
    # If deleted successfully
    if delete_result != None and delete_result.acknowledged:
        return True
    else:
        return False

# Return a vehicle with a randomly generated vin, random type, random color,
# random name based on this randomly generated information
def generate_random_vehicle():
    vin = vin_generator.VIN().get_vin()
    vehicle_type = random.choice(list(Vehicle_Type)).name
    
    available_vehicle_colors = ["RED", "BLUE", "WHITE", "GRAY", "BLACK", "YELLOW", "SEA_FORM_GREEN", "CAMO"]

    vehicle_color = random.choice(available_vehicle_colors)
    vehicle_name = generate_vehicle_name(vin, vehicle_type, vehicle_color)

    return Vehicle (vin, vehicle_name, vehicle_type, vehicle_color)

# Return a string of a vehicle name that is generated from the vin,
# vehicle type, and vehicle color
def generate_vehicle_name(vin, vehicle_type, vehicle_color):
    serial_number = vin[9:]
    vehicle_type_letter = vehicle_type[0]
    vehicle_color_letter = vehicle_color[0]
    random_number_sequence = str(int(random.random() * 9)) + str(int(random.random() * 9)) + str(int(random.random() * 9))
    name = "A" + vehicle_type_letter + "-" + vehicle_color_letter + random_number_sequence + "-" + serial_number

    return name

# take a dictionary and turn it into a fleet
def create_fleet_object(dictionary):
    if ("fleet_name" not in dictionary):
        return None
    if ("fleet_region" not in dictionary):
        return None
    if ("fleet_vehicles" not in dictionary):
        return None
    if ("warehouses" not in dictionary):
        return None
    return Fleet (dictionary["fleet_name"] , dictionary["fleet_region"], dictionary["fleet_vehicles"], dictionary["warehouses"])


# https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
# output the distance between two coordinates in kilometers
def calculate_distance (latlong1, latlong2):
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

def determine_nearest_vehicle (available_vehicles, starting_position):
    closest_distance = 0
    if len(available_vehicles) > 0:
        closest_distance = calculate_distance (available_vehicles[0]["vehicle_position"], starting_position)
        selected_vehicle = available_vehicles[0]
        for index in range (1, len (available_vehicles)):
            distance = calculate_distance (available_vehicles[index]["vehicle_position"], starting_position)
            if closest_distance > distance:
                closest_distance = distance
                selected_vehicle = available_vehicles[index]
    else:
        return None
            
    return selected_vehicle