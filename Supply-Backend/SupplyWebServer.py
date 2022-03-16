# Web server to run the backend!
# Team 12
# Made by Will Luong, Colby Tang, Erik Hernandez, Jeffrey Quade

#####################
# SUPPLY WEB SERVER #
#####################

import http.server
from http.server import BaseHTTPRequestHandler
import json
import requests
import urllib.parse

from supply_vehicle import Vehicle
from supply_fleet import Fleet
from supply_database_utils import Supply_Database_Utils

import supply_api_vehicle

class SupplyHTTPRequestHandler(BaseHTTPRequestHandler):
    database_utils = Supply_Database_Utils()
        
    # function to handle POST request to a server
    # a POST request got sent in as a parameter
    def do_POST(self):
        print ("\n******** NEW SUPPLY POST REQUEST *********")
        # get the path of the request that was sent in
        path = self.path
        
        # Displaying the headers of the paht being sent in
        print('Headers:"', self.headers, '"')

        # Displaying the type of the content of the request
        print('Content-Type:', self.headers['content-type'])
        
        # Collecting the length of the body read the characters
        # that are contained in the body.
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        
        # convert body into a dictionary if the content-type is a json object
        incoming_dictionary = None
        if "json" in str(self.headers['content-type']):
            incoming_dictionary = json.loads(body)
            print ("Incoming Dictionary: " + str(incoming_dictionary))

        # Handling a request vehicle request
        if path == "/api/backend/requestvehicle":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            
            print ("Request Vehicle API:")
            response = supply_api_vehicle.request_vehicle(incoming_dictionary)
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code(403, 'Could not find available vehicle, Code 403')

        # Handling a generate vehicle request
        elif path == "/api/backend/generatevehicle":           
            print ("Generate Vehicle API:")
            # randomly generate a new vehicle
            new_vehicle = supply_api_vehicle.generate_random_vehicle()           
            vehicle_name = new_vehicle.dictionary["vehicle_name"]
            vehicle_vin = new_vehicle.dictionary["vin"]
            
            # register vehicle
            response = supply_api_vehicle.register_vehicle(new_vehicle)
            
            if response:
                self.respond_code(200, "Vehicle" + vehicle_name + " entered into database! (VIN:" + vehicle_vin + ")")
            else:
                self.respond_code(403, "Vehicle " + vehicle_name + " already exists in the database! (VIN:" + vehicle_vin + ")")
                
        # Generate vehicle name for front end using vin, vehicle_type, and vehicle_color
        elif path == "/api/backend/generatevehiclename":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            print ("Generate Vehicle Name API:")
            # randomly generate a new vehicle
            vehicle_name = supply_api_vehicle.generate_vehicle_name(
                incoming_dictionary["vin"], 
                incoming_dictionary["vehicle_type"],
                incoming_dictionary["vehicle_color"]
            )
            
            # register vehicle
            response = vehicle_name
            if response:
                self.respond_code(200, response)
            else:
                self.respond_code(400, "Vehicle name could not be generated!")
                
        # Register new vehicle, check if vehicle already exists in database
        elif path == "/api/backend/registervehicle":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            
            print ("Register Vehicle API:")
            new_vehicle = Vehicle(
                incoming_dictionary["vin"], 
                incoming_dictionary["vehicle_name"],
                incoming_dictionary["vehicle_type"],
                incoming_dictionary["vehicle_color"]
                )
            response = supply_api_vehicle.register_vehicle(new_vehicle) 
            
            if response:
                self.respond_code(200, "Vehicle" + new_vehicle.vehicle_name + " entered into database! (VIN:" + new_vehicle.vin + ")")
            else:
                self.respond_code(403, "Vehicle " + new_vehicle.vehicle_name + " already exists in the database! (VIN:" + new_vehicle.vin + ")")

        # Remove vehicle from database based on the vin
        elif path == "/api/backend/removevehicle":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            
            print ("Remove Vehicle API:")
            vin = incoming_dictionary["vin"]
            response = supply_api_vehicle.remove_vehicle(vin)
            
            if response:
                self.respond_code(200, "Vehicle " + vin + " deleted")
            else:
                self.respond_code(400, "Could not delete vehicle: " + vin)
        
        # Grab dispatch record
        elif path == "/api/backend/fetchdispatch":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            
            print ("Fetch Dispatch API:")
            response = self.database_utils.get_dispatch_from_id (incoming_dictionary["dispatch_id"])
            
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code(404, "Could not get dispatch! Code 404")
            
        # Grab fleet record
        elif path == "/api/backend/fetchfleet":
            if incoming_dictionary == None:
                self.respond_code(400, "No JSON object found!")
                return
        
            print ("Fetch Fleet API:")
            response = self.database_utils.get_fleet_from_id (incoming_dictionary["fleet_id"])
            
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code(400, "Could not get fleet!")
                
        # Modify fleet
        elif path == "/api/backend/fleet":
            # Check if there's a json object
            if incoming_dictionary == None:
                self.respond_code(400, "No JSON object found!")
                return
        
            print ("Modify Fleet API:")
            # Check for a command
            if "command" not in incoming_dictionary:
                self.respond_code(400, "No command in fleet request found!")
                return
            
            command = incoming_dictionary["command"]
            
            # Check if command is a string
            if type(command) != str:
                self.respond_code(400, "Command is not a string!")
                return
            
            
            # if command is to add a fleet
            if command.upper() == "ADD":
                
                # create a fleet object
                fleet_object = self.create_fleet_object(incoming_dictionary)
                if fleet_object == None:
                    self.respond_code(400, "Fleet object could not be created from the request!")
                    return
            
                response = self.database_utils.insert_fleet (fleet_object)
                if response != None:
                    self.respond_code (200, "Inserted fleet! ID: " + str(response.inserted_id))
                else:
                    self.respond_code(400, "Could not insert fleet!")
            
            elif command.upper() == "REMOVE":
                response = self.database_utils.remove_fleet (incoming_dictionary["fleet_name"])
                if response != None:
                    self.respond_code (200, "Removed fleet " + incoming_dictionary["fleet_name"] + "!")
                else:
                    self.respond_code(400, "Could not remove fleet!")
                    
            elif command.upper() == "UPDATE":
                # create a fleet object
                fleet_object = self.create_fleet_object(incoming_dictionary)
                if fleet_object == None:
                    self.respond_code(400, "Fleet object could not be created from the request!")
                    return
                
                response = self.database_utils.update_fleet (fleet_object)
                if response != None:
                    self.respond_code (200, "Updated fleet " + fleet_object.fleet_name + "!")
                else:
                    self.respond_code(400, "Could not update fleet!")
                    
            else:
                self.respond_code(400, "Could not understand command!")
                                
        #elif path == "/api/backend/validateaddress":
        
        # Connection error:
        else:
            # If the path did not match any known request
            # a 404 Not Found error is thrown.
            print ("api/backend failed")
            self.respond_code(404, 'Path did not match any known request! Code 404')

    # function to deal with a GET request:
    def do_GET(self):
        print ("\n******** NEW SUPPLY GET REQUEST *********")
        print ("GET REQUEST self.path: " + self.path)
        split_path = self.path.split('?', 1)
        if 'api/backend' in split_path[0]:
            # parse the URL for parameters
            params = urllib.parse.parse_qs(split_path[1])
            
            # for debugging purpose:
            print("Params: " + str(params))
            
            # retrieving all vehicles
            if "vehicle-all" in params:
                response = self.database_utils.get_all_vehicles()
                
            # retrieving a vehicle through its name
            elif "vehicle-name" in params:
                param = params['vehicle-name'][0]
                response = self.database_utils.get_vehicle_from_name(param)
                
            # retrieving a vehicle through its type
            # can also retrieve available vehicle of type
            elif "vehicle-type" in params:
                vehicle_type = params['vehicle-type'][0]
                if "get" in params:
                    if params['get'][0] == "available":
                        response = self.database_utils.get_available_vehicle_from_type(vehicle_type)
                    else:
                        response = self.database_utils.get_vehicle_from_type(vehicle_type)
                else:
                    response = self.database_utils.get_vehicle_from_type(vehicle_type)
                    
            # retrieving a vehicle through its id
            elif "vehicle-id" in params:
                vehicle_id = params["vehicle-id"][0]
                response = self.database_utils.get_vehicle_from_id(vehicle_id)
                
            # Check quickly if server is running
            elif "status" in params:
                response = "Supply Web Server running! (200)"
                
            else:
                response = None
            
            # Handle the response
            print("Response: " + str(response))
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code (403, "Could not find any params!")
        else:
            # Send a 404 Error handling if the route does not exist
            self.respond_code (404, "Route does not exist!")
            
    def do_OPTIONS(self):
        self.send_response(200, "ok")     
        self._send_cors_headers()  
            
    # Converts python dictionary into a json object and sends it with a code
    def respond_convert_json_object (self, code, dictionary):
        # Define the response code and the headers
        self.send_response(code)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')

        # Signify that you are done sending the headers:
        self.end_headers()
        
        # convert python dictionary into a JSON object
        # encode json_object into utf_8
        self.wfile.write(json.dumps(dictionary).encode(encoding='utf_8'))
    
    # Responds with a simple code and response
    def respond_code (self, code, response):
        self.send_response(code)
        self._send_cors_headers()
        self.end_headers()
        bytesStr = response.encode('utf-8')
        
        self.wfile.write(bytesStr)
    
    # Sets headers required for CORS 
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type, X-Requested-With")

# Execute the web server:
def main():
    # Server port
    port = 4012

    # Create server
    httpServer = http.server.HTTPServer(('', port), SupplyHTTPRequestHandler)
    print("Supply running on port", port)

    # Start server, use CTRL+C to close it.
    try:
        httpServer.serve_forever()
    except KeyboardInterrupt:
        httpServer.server_close()
        print ("Supply server close")

if __name__ == "__main__":
    main()