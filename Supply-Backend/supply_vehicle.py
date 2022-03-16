from enum import Enum

# Class: Vehicle
# Concern: Supply
# Required parameters:
    # vin - String: Vehicle Identification Number
    # vehicle_name - String: Name of vehicle
    # vehicle_type - Vehicle_Type -> String: Type of the vehicle such as Bus, Van, Truck
    # vehicle_color - Vehicle_Color -> String: Color of the vehicle, such as Red, Blue, Green

# Optional parameters:
    # vehicle_position - [Float, Float]: The current position of the vehicle in latitude and longtitude pairs.
    # vehicle_status - String: The current position of the vehicle in latitude and longtitude pairs.
    # fleet_id - String: ID of the fleet that the vehicle is assigned to

####################### testing methods ####################################
#new_vehicle = Vehicle("13rqwefasdfqefrqw", "Honda", "bus", "gray", True)

#print(new_vehicle.dictionary)
#############################################################################

class Vehicle:
    status_ok = "AVAILABLE"
    status_otw = "OTW"
    status_done = "DONE"
    status_offline = "OFFLINE"
    accepted_status = [status_ok, status_otw, status_done, status_offline]

    def __init__ (self, vin, vehicle_name, vehicle_type, vehicle_color):
        self.vin = vin
        self.vehicle_name = vehicle_name
        self.vehicle_type = vehicle_type
        self.vehicle_color = vehicle_color
        self.vehicle_status = self.status_offline
        # default position for vehicle is warehouse edwards (St. Edward's University)
        self.vehicle_position = [
                -97.7537396402663,
                30.230308745781883
            ]
        self.fleet_id = ""

    # getter method for vin
    @property
    def vin(self):
        return self._vin

    # setter method for vin
    @vin.setter
    def vin(self, value):
        self._vin = value

    # getter method for vehicle name
    @property
    def vehicle_name(self):
        return self._vehicle_name

    @vehicle_name.setter
    def vehicle_name(self, value):
        self._vehicle_name = value

    # getter method for vehicle type
    @property
    def vehicle_type(self):
        return self._vehicle_type.name

    # setter method to set vehicle type, checks for enum
    @vehicle_type.setter
    def vehicle_type(self, v_type):
        if (type(v_type) == int):
            #print ("Vehicle Type, received an int")
            self._vehicle_type = Vehicle_Type(v_type)
        elif (type(v_type) == Vehicle_Type):
            #print ("Vehicle Type, received an enum")
            self._vehicle_type = v_type
        elif type(v_type) == str:
            #print ("Vehicle Type, received an str")
            self._vehicle_type = Vehicle_Type[v_type.upper()]
        else:
            print ("VEHICLE CLASS ERROR: Could not set vehicle color! Neither enum, string, nor int")
            raise Exception("Type: " + v_type)

    # getter method for vehicle color
    @property
    def vehicle_color(self):
        return self._vehicle_color

    # setter method to set vehicle type, checks for enum
    @vehicle_color.setter
    def vehicle_color(self, v_color):
        if type(v_color) == str:
            self._vehicle_color = v_color.upper()
        else:
            print ("VEHICLE CLASS ERROR: Could not set vehicle color! Not a string!")
            raise Exception("Color: " + str(v_color))

    # getter method for vehicle position
    @property
    def vehicle_position(self):
        return self._vehicle_position

    # setter method for vehicle position
    @vehicle_position.setter
    def vehicle_position(self, value):
        #print (type(value))
        #print (type(value[0]))
        if type(value) == list and type(value[0]) == float:
            self._vehicle_position = value
        else:
            raise Exception("Position needs to be a [Float]: " + str(value))

    # getter method for vehicle position
    @property
    def vehicle_status(self):
        return self._vehicle_status

    # setter method for vehicle position
    @vehicle_status.setter
    def vehicle_status(self, value):
        if type(value) != str:
            raise Exception("ERROR: " + str(value) + " is not a string!")
        elif value.upper() in self.accepted_status:
            self._vehicle_status = value.upper()
        else:
            raise Exception("ERROR: " + str(value) + " is not accepted")
    
    # getter method for fleet id
    @property
    def fleet_id(self):
        return self._fleet_id
        
    # setter method for fleet id
    @fleet_id.setter
    def fleet_id(self, id):
        self._fleet_id = id

    # getter method for all values of vehicle
    @property
    def dictionary(self):
        vehicle_dictionary = {
            "vin": self.vin,
            "vehicle_name": self.vehicle_name,
            "vehicle_type": self.vehicle_type,
            "vehicle_color": self.vehicle_color,
            "vehicle_position": self.vehicle_position,
            "vehicle_status": self.vehicle_status,
            "fleet_id": self.fleet_id
        }
        return vehicle_dictionary

class Vehicle_Type(Enum):
    BUS = 0
    TRUCK = 1
    VAN = 2