import http.server
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

import supply_api_heartbeat

class HeartbeatListener(BaseHTTPRequestHandler):
    def do_POST(self):
        print ("\n******** NEW HEARTBEAT POST REQUEST *********")
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
        
        # convert body into a dictionary
        incoming_dictionary = None
        if "json" in str(self.headers['content-type']):
            incoming_dictionary = json.loads(body)
            print ("Incoming Dictionary: " + str(incoming_dictionary))
            print ("Incoming Dictionary Type: ", type(incoming_dictionary))
        print ("POST PATH: ", path)
        
        # Handling a registration request from POST
        if path == "/api/heartbeat/requestbeat":
            if incoming_dictionary == None:
                self.respond_code(404, "No JSON object found!")
                return
            print ("Heartbeat API:")
            response = supply_api_heartbeat.request_beat(self, incoming_dictionary)
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code(403, "Not a valid heartbeat! Code 403")
                
        #Connection error:
        else:
            # If the path did not match any known request
            # a 404 Not Found error is thrown.
            print ("api/heartbeat failed")
            self.respond_code(404, 'Path did not match any known request! Code 404')
            
    def do_GET(self):
        print ("\n******** NEW HEARTBEAT GET REQUEST *********")
        print ("GET REQUEST self.path: " + self.path)
        print ("COMMON SERVICES SERVER NAME:", self.server.server_name)
        split_path = self.path.split('?', 1)
        if 'api/heartbeat' in split_path[0]:
            #db_utils = self.create_db_object()
            # parse the URL for parameters
            params = urllib.parse.parse_qs(split_path[1])
            
            # for debugging purpose:
            print("Params: " + str(params))
            # Check quickly if server is running
            if "status" in params:
                response = "Heartbeat listener running! (200)"
            else:
                response = None
                
            # Handle the response
            print("Response: " + str(response))
            if response != None:
                self.respond_convert_json_object (200, response)
            else:
                self.respond_code (403, "Could not find any valid params!")
                
        else:
            #Send a 404 Error handling if the route does not exist
            self.respond_code(404, "Route does not exist")
            
    # Converts python dictionary into a json object and sends it with a code
    def respond_convert_json_object (self, code, dictionary):
        print ("Respond Convert JSON Object:", code, dictionary)
        # Define the response code and the headers
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")

        # Signify that you are done sending the headers:
        self.end_headers()
        
        # convert python dictionary into a JSON object
        # encode json_object into utf_8
        self.wfile.write(json.dumps(dictionary).encode(encoding='utf_8'))
    
    # Responds with a simple code and response
    def respond_code (self, code, response):
        print ("Respond Code:", code, response)
        self.send_response(code)
        self.end_headers()
        bytesStr = response.encode('utf-8')
        self.wfile.write(bytesStr)
        
# Execute the web server:
def main():
    # Server port
    port = 4212

    # Create server
    httpServer = http.server.HTTPServer(('', port), HeartbeatListener)
    print("Heartbeat running on port", port)

    # Start server, use CTRL+C to close it.
    try:
        httpServer.serve_forever()
    except KeyboardInterrupt:
        httpServer.server_close()
        print ("Heartbeat listener close")


if __name__ == "__main__":
    main()