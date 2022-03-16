import json
from supply_database_utils import Supply_Database_Utils
from supply_vehicle import Vehicle
from supply_fleet import Fleet
from mapping_services import Mapping_Services

# Heartbeat request
def request_beat (self, dictionary):
    vehicle_id = dictionary["vehicle_id"]
    vehicle_status = dictionary["vehicle_status"]
    vehicle_position = dictionary["vehicle_position"]
    dispatch_id = None
    if "dispatch_id" in dictionary:
        dispatch_id = dictionary["dispatch_id"]
    
    database_utils = Supply_Database_Utils()
    requester_vehicle = database_utils.get_vehicle_from_id (vehicle_id)
    
    if requester_vehicle != None:
        fleet_id = requester_vehicle["fleet_id"]
    else:
        return None
    
    print ("Heartbeat from vehicle", vehicle_id, vehicle_status, vehicle_position)
    
    accepted_vehicle_statuses = Vehicle.accepted_status
    
    # If vehicle status is not valid, return None
    if vehicle_status not in accepted_vehicle_statuses:
        return None
    
    # update vehicle position and status in db
    database_utils.update_vehicle_values(vehicle_id, 
        {
        "vehicle_position": vehicle_position,
        "vehicle_status": vehicle_status,
        "time_reported": database_utils.get_milliseconds(), 
        "time_reported_date": database_utils.get_timestamp()
        }
    )

    # if vehicle is available
    if vehicle_status == "AVAILABLE":
        return check_and_send_on_dispatch (database_utils, vehicle_id, vehicle_position)
    
    # if vehicle is on the way
    elif vehicle_status == "OTW":
        return {"response": "CONTINUE ROUTE"}

    # if vehicle is done with dispatch
    elif vehicle_status == "DONE":
        # update dispatch status
        if dispatch_id is not None:
            database_utils.update_dispatch_status (dispatch_id, {"dispatch_status": "COMPLETED"})
            
        # check for more dispatches
        response = check_and_send_on_dispatch (database_utils, vehicle_id, vehicle_position)
        if response["response"] == "DISPATCH":
            return response
        else:
            # if no more dispatches, return to closest warehouse
            # if no fleet, just stand still
            fleet_dictionary = database_utils.get_fleet_from_id (fleet_id)
            if fleet_dictionary != None:
                fleet = create_fleet_object (fleet_dictionary)
                warehouse = fleet.get_closest_warehouse (vehicle_position)
                directions = get_vehicle_directions ([warehouse["coordinates"]], vehicle_position)
                response_dictionary = {"response": "RETURN", "route": directions, "warehouse_name": warehouse["warehouse_name"]}
                return directions
            return {"response": "STANDBY"}

    # if vehicle is under maintenance
    elif vehicle_status == "MAINT":
        return {"response": "COOL"}
    
    # if vehicle sent a gibberish request
    else:
        return {"response": "WHAT"}

def determine_dispatch (dispatches):
    dispatch = dispatches[0]
    for entry in dispatches:
        if entry["start_timestamp_ms"] < dispatch["start_timestamp_ms"]:
            dispatch = entry
    return dispatch

def get_vehicle_directions (stops, vehicle_position):
    stops.insert(0, vehicle_position)
    mapping_service = Mapping_Services (stops)
    return mapping_service.get_directions()

def check_and_send_on_dispatch (db, vehicle_id, vehicle_position):
    dispatches = db.get_open_dispatches_with_vid(vehicle_id)
    print ("dispatches " + str(dispatches))
    
    # if a dispatch is available for a vehicle
    if len(dispatches) > 0:
        # Determine oldest dispatch through milliseconds
        dispatch = determine_dispatch (dispatches)
        db.update_dispatch_status (dispatch["_id"], {"dispatch_status": "IN_PROGRESS"})
        stops = dispatch["stops"]
        vehicle_route = get_vehicle_directions(stops, vehicle_position)
        response_dictionary = {"response": "DISPATCH", "route": vehicle_route.directions, "dispatch_id": dispatch["_id"]}
        return response_dictionary
    else:
        return {"response": "COOL"}

# create a fleet object from dictionary
def create_fleet_object (dictionary):
    if dictionary["fleet_name"] != None:
        fleet_name = dictionary["fleet_name"]
    else:
        raise Exception ("No fleet name!")
    
    if dictionary["fleet_region"] != None:
        fleet_region = dictionary["fleet_region"]
    else:
        raise Exception ("No fleet region!")
    
    if dictionary["fleet_vehicles"] != None:
        fleet_vehicles = dictionary["fleet_vehicles"]
    else:
        raise Exception ("No fleet vehicles!")

    if dictionary["warehouses"] != None:
        warehouses = dictionary["warehouses"]
    else:
        raise Exception ("No warehouses!")
    
    return Fleet(fleet_name, fleet_region, fleet_vehicles, warehouses)