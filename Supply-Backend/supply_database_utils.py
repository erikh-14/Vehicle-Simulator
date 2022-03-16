# Team 12
# Written by Will
# Changed by Colby Tang, Erik Hernandez

## __supplydb Collections__

### Dispatches
#   _id - ObjectId: The id assigned when inserted into the database
#   start_timestamp - String: Time the vehicle started the order in MM-DD-YYYY: HH:MM:SS
#   tops - [String, String]: A list of stops for the route
#   route - [[Float, Float]]: Array of coordinates in the route
#   order_id - String: ID of the order that is assigned to the dispatch
#   vehicle_id - String: ID of the vehicle that is carrying out the dispatch
#   end_timestamp - String: Time the vehicle finishes the order in MM-DD-YYYY: HH:MM:SS
#   dispatch_status - Dispatch_Status -> String: Status of the dispatch
#       NOT_COMPLETED = 0
#        IN_PROGRESS = 1
#        COMPLETED = 2
#        CANCELED = 3

### Vehicles
#    _id - ObjectId: The id assigned when inserted into the database
#    vin - String: Vehicle Identification Number
#    vehicle_name - String: Name of vehicle
#    vehicle_type - Vehicle_Type -> String: Type of the vehicle such as Bus, Van, Truck
#    vehicle_color - Vehicle_Color -> String: Color of the vehicle, such as Red, Blue, Green
#    is_available - Bool: Is the vehicle available for service?
#    vehicle_position - [Float, Float]: The current position of the vehicle in latitude and longtitude pairs.

### Fleets
#    _id - ObjectId: The id assigned when inserted into the database
#    fleet_name - String: Name of the fleet
#    fleet_region - String: Service region of the fleet
#    fleet_size - Int: Size of the fleet, adjust upon assigning vehicles from the fleet.
#    warehouses - [{"warehouse_name": String, "coordinates": [Float,Float]]: Array of dictionaries for warehouses

import pymongo
import datetime
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

from supply_vehicle import Vehicle

class Supply_Database_Utils:
    # Making a connection to a database with MongoClient from pymongo
    # Opens a connection
    def __init__(self, uri="mongodb://team12:password@localhost:6012/admin"): 
        self.uri = uri
        self.client = MongoClient(uri)
        self.db = self.client.supplydb
        self.time_format = "%Y-%m-%d %H:%M:%S"
    
    # Retrieving a collection called dispatches in the database
    def get_dispatches_collection(self):
        return self.db.dispatches

    # Retrieving a collection called vehicles in the database
    def get_vehicles_collection(self):
        return self.db.vehicles
    
    # Retrieving a collection called dispatches in the database
    def get_fleets_collection(self):
        return self.db.fleets
    
    # retrieve the current time in YYYY-MM-DD HH:MM:SS
    def get_timestamp(self):
        return datetime.datetime.now().strftime(self.time_format)
    
    # retrieve the current time in milliseconds for determining the newest/oldest
    def get_milliseconds(self):
        return int(round(time.time() * 1000))
    
    # called when object is deleted
    def __delete__(self):
        self.client.close()

    # check if an objectid is valid
    def validate_objectid(self, objectid):
        return ObjectId.is_valid (objectid)
    
############
# DISPATCH #
############

    # insert dispatch into database
    def insert_dispatch(self, dispatch):
        collection = self.get_dispatches_collection()
        dispatch_dictionary = dispatch.dictionary
        dispatch_dictionary.update( {"start_timestamp": self.get_timestamp()})
        dispatch_dictionary.update( {"start_timestamp_ms": self.get_milliseconds()})
        insert_one_result = collection.insert_one(dispatch_dictionary)

        # if insertion is successful, take the dispatch id and insert it into the object
        if insert_one_result.acknowledged:
            dispatch.id = str(insert_one_result.inserted_id)

        return insert_one_result

    # update dispatch with dispatch object
    def update_dispatch(self, dispatch):
        dispatch_dictionary = dispatch.dictionary
        collection = self.get_dispatches_collection()

        dispatch_id = dispatch.id

        query = {"_id": ObjectId(dispatch_id)}
        new_values = { "$set": 
            {
            "vehicle_id": dispatch_dictionary["vehicle_id"], 
            "end_timestamp": dispatch_dictionary["end_timestamp"], 
            "route": dispatch_dictionary["route"],
            "dispatch_status": dispatch_dictionary["dispatch_status"]
            }
        }
        dispatch_update = collection.update_one(query, new_values)

        return dispatch_update

    # retrieve dispatch from database
    def get_dispatch_from_id(self, id):
        if not self.validate_objectid(id):
            return None
        collection = self.get_dispatches_collection()

        entry = collection.find_one({'_id': ObjectId(id)})

        if entry != None:
            entry['_id'] = str(entry['_id'])
            return entry
        else:
            return None
    
    # retrieve dispatch from database
    def update_dispatch_status(self, id, status):
        collection = self.get_dispatches_collection()
        
        query = {"_id": ObjectId(id)}
        new_values = {"$set": {"dispatch_status": status}}
        dispatch_update = collection.update_one(query, new_values)
        
        return dispatch_update
    
    # checks if vehicle has dispatches assigned to it
    # used in heartbeat
    # returns an array of dictionaries, None if none found
    def get_dispatches_with_vid(self, vid):
        if not self.validate_objectid(vid):
            return None
        collection = self.get_dispatches_collection()
        cursor = collection.find({'vehicle_id': vid})
        
        if cursor != None:
            result = []
            for entry in cursor:
                entry['_id'] = str(entry['_id'])
                result.append(entry)
            return result
        else:
            return None
        
    # checks if vehicle has dispatches assigned to it
    # used in heartbeat
    # returns an array of dictionaries, None if none found
    def get_open_dispatches_with_vid(self, vid):
        if not self.validate_objectid(vid):
            return None
        collection = self.get_dispatches_collection()
        cursor = collection.find({'vehicle_id': vid, 'dispatch_status':"NOT_COMPLETED"})
        
        if cursor != None:
            result = []
            for entry in cursor:
                entry['_id'] = str(entry['_id'])
                result.append(entry)
            return result
        else:
            return None
    
    def get_open_dispatches(self):
        collection = self.get_dispatches_collection()
        cursor = collection.find({'dispatch_status': "NOT_COMPLETED"})
        
        if cursor != None:
            result = []
            for entry in cursor:
                entry['_id'] = str(entry['_id'])
                result.append(entry)
            return result
        else:
            return None
    
###########
# VEHICLE #
###########

    # Is vehicle in database? Use vin to match
    def does_vin_exist(self, vehicle_vin):
        collection = self.get_vehicles_collection()

        find_one_result = collection.find_one({'vin': vehicle_vin}, {'vin': 1})

        if find_one_result != None:
            return True
        else:
            return False
    
    # insert vehicle into database
    def insert_vehicle(self, vehicle):
        collection = self.get_vehicles_collection()
        vehicle_dictionary = vehicle.dictionary

        is_matching = self.does_vin_exist (vehicle_dictionary['vin'])
        if is_matching:
            insert_one_result = None
        else:
            insert_one_result = collection.insert_one(vehicle_dictionary)

        return insert_one_result

    # insert vehicle into database
    def delete_vehicle_using_vin(self, vin):
        collection = self.get_vehicles_collection()

        if self.does_vin_exist (vin):
            result = collection.delete_one({"vin": vin})
        else:
            result = None

        return result
    
    # grab vehicle based on query
    def get_vehicle (self, query):
        collection = self.get_vehicles_collection()
        result = collection.find_one(query)
        if result != None:
            result['_id'] = str(result['_id'])
            return result
        else:
            return None
        
    # grab multiple vehicles based on query
    def get_multiple_vehicles (self, query):
        collection = self.get_vehicles_collection()
        cursor = collection.find(query)
        if cursor != None:
            result = []
            for entry in cursor:
                entry['_id'] = str(entry['_id'])
                result.append(entry)
            return result
        else:
            return None

    # grab all vehicle info from finding the name
    def get_vehicle_from_name(self, name):
        return self.get_vehicle({'vehicle_name':name})

    # grab all vehicle info from finding the type
    def get_vehicle_from_type(self, vehicle_type):
        return self.get_vehicle({'vehicle_type':vehicle_type.upper()})

    # grab all vehicle info from finding the type and availability
    def get_available_vehicle_from_type(self, vehicle_type):
        return self.get_vehicle({'vehicle_type':vehicle_type.upper(), 'vehicle_status': Vehicle.status_ok})
    
    # grab all vehicle info from finding the type and availability
    def get_available_vehicles_from_type(self, vehicle_type):
        return self.get_multiple_vehicles({'vehicle_type':vehicle_type.upper(), 'vehicle_status': Vehicle.status_ok})
        
    # grab all vehicle info from finding the id
    def get_vehicle_from_id(self, vid):
        if not self.validate_objectid(vid):
            return None
        return self.get_vehicle({"_id": ObjectId(vid)})
    
    # grab all vehicle info from finding the name
    # returns an array of dictionaries or None
    def get_all_vehicles(self):
        return self.get_multiple_vehicles({})
    
    # Take the vehicle object and update its entry in the database
    def update_vehicle(self, vehicle):
        vehicle_dictionary = vehicle.dictionary
        collection = self.get_vehicles_collection()

        vehicle_id = vehicle.id

        query = {"_id": ObjectId(vehicle_id)}
        new_values = { "$set": 
            {
            "vin": vehicle_dictionary["vin"],
            "vehicle_name": vehicle_dictionary["vehicle_name"],
            "vehicle_type": vehicle_dictionary["vehicle_type"],
            "vehicle_color": vehicle_dictionary["vehicle_color"],
            "vehicle_position": vehicle_dictionary["vehicle_position"]
            }
        }
        update = collection.update_one(query, new_values)

        return update

    # Take the vehicle id and update its vehicle status and position in the database
    def update_vehicle_values(self, vid, new_values):
        collection = self.get_vehicles_collection()
        
        query = {"_id": ObjectId(vid)}
        fields = { "$set": new_values}
        update = collection.update_one(query, fields)

        return update
    
    def update_vehicle_heartbeat(self, vid):
        return update_vehicle_values(vid, {"time_reported": self.get_milliseconds(), "time_reported_date": self.get_timestamp()})
    
#########
# FLEET #
#########

    # does fleet already exist in the database?
    def does_fleet_exist (self, id):
        if not self.validate_objectid(id):
            return None
        collection = self.get_fleets_collection()

        find_one_result = collection.find_one({'_id': ObjectId(id)}, {'_id': 1})

        if find_one_result != None:
            return True
        else:
            return False

    # Retrieve a fleet object with the id
    def get_fleet_from_id(self, id):
        if not self.validate_objectid(id):
            return None
        collection = self.get_fleets_collection()

        entry = collection.find_one({'_id': ObjectId(id)})

        if entry != None:
            entry['_id'] = str(entry['_id'])
            return entry
        else:
            return None
        
    # Insert a fleet
    def insert_fleet(self, fleet_object):
        collection = self.get_fleets_collection()
        fleet_name = fleet_object.fleet_name
        is_matching = self.does_fleet_exist (fleet_name)
        if is_matching:
            insert_one_result = None
        else:
            insert_one_result = collection.insert_one(fleet_object.dictionary)

        return insert_one_result
    
    # Remove a fleet through its name
    def remove_fleet(self, fleet_name):
        collection = self.get_fleets_collection()
        if self.does_fleet_exist ():
            result = collection.delete_one({"fleet_name": fleet_name})
        else:
            result = None

        return result
        
    # Update fleet with fleet object
    def update_fleet(self, fleet_object):
        collection = get_fleets_collection()
        fleet_dictionary = fleet_object.dictionary
        
        query = {"_id": ObjectId(fleet_object.id)}
        new_values = { "$set": 
            {
                "fleet_name": fleet_object.fleet_name,
                "fleet_region": fleet_object.fleet_region,
                "fleet_size": fleet_object.fleet_size,
                "fleet_vehicles": fleet_object.fleet_vehicles,
                "warehouses": fleet_object.warehouses
            }
        }
        fleet_update = collection.update_one(query, new_values)
        
        return fleet_update