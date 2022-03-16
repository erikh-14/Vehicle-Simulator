# MongoDB Supply-Side Documentation

Version 1.0

Author: Colby Tang

## __What is MongoDB?__

MongoDB is a cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB uses JSON-like documents with schema. MongoDB is developed by MongoDB Inc. and licensed under the Server Side Public License ( *Wikipedia* ).

The hierarchy of a MongoDB database is as follows:

* Database
    * Collection
        * Document

In other words:

* A **database** holds many collections.
* A **collection** holds many documents.

Each collection should be storing only one kind of document, e.g. a vehicle. You would create another collection for a dispatch. Each entry inside the vehicle collection is called a document. Vehicle A and Vehicle B would be two different documents.

## __How to access the MongoDB database__

We are accessing our MongoDB by using SSH (Secure Shell) to connect to our Supply server. Once logged in, we need to login into the database. This database is separate from the Demand database.

To log into the database we use a handy symlink, or a shortcut: 
```
database-login
```

It will prompt you for a password. Default password is password.

The symlink is short for:
```
mongo --port 6012 -u team12 -p --authenticationDatabase admin
```

## __supplydb Collections__

### Vehicles
    _id - ObjectId: The id assigned when inserted into the database
    vin - String: Vehicle Identification Number
    vehicle_name - String: Name of vehicle
    vehicle_type - Vehicle_Type -> String: Type of the vehicle such as Bus, Van, Truck
    vehicle_color - Vehicle_Color -> String: Color of the vehicle, such as Red, Blue, Green
    is_available - Bool: Is the vehicle available for service?
    vehicle_position - [Float, Float]: The current position of the vehicle in latitude and longtitude pairs.

### Dispatches
    _id - ObjectId: The id assigned when inserted into the database
    start_timestamp - String: Time the vehicle started the order in MM-DD-YYYY: HH:MM:SS
    stops - [String, String]: A list of stops for the route
    route - [[Float, Float]]: Array of coordinates in the route
    order_id - String: ID of the order that is assigned to the dispatch
    vehicle_id - String: ID of the vehicle that is carrying out the dispatch
    end_timestamp - String: Time the vehicle finishes the order in MM-DD-YYYY: HH:MM:SS
    dispatch_status - Dispatch_Status -> String: Status of the dispatch
        NOT_COMPLETED = 0
        IN_PROGRESS = 1
        COMPLETED = 2
        CANCELED = 3

### FM (Fleet Manager)
    _id - ObjectId: The id assigned when inserted into the database
    username - String: Used during login
    password - String: Used during login
    first_name - String: Displayed in the dashboard
    last_name - String: Displayed in the dashboard
    email - String: To contact the fleet manager
    country - String: Country of residence
    phone_number - String: To contact the fleet manager

### Fleets
    _id - ObjectId: The id assigned when inserted into the database
    fleet_name - String: Name of the fleet
    fleet_region - String: Service region of the fleet
    fleet_size - Int: Size of the fleet, adjust upon assigning vehicles from the fleet.
    warehouse_locations - [[Float,Float]]: Array of coordinates for warehouse locations


## __Useful MongoDB Commands__

### **List all databases**

This will show all the databases in the database server.

#### Command
```
show dbs
```

#### Example
```
> show dbs
admin     0.000GB
config    0.000GB
local     0.000GB
supplydb  0.000GB
```

### **Select a database**

Tell MongoDB which database you'll be using. Our current database is *supplydb*.

#### Command
```
use supplydb
```

#### Example
``` 
use supplydb
switched to db supplydb
```

### **List all collections in the selected database**

#### Command
```
db.getCollectionNames()
```

#### Example
```
> db.getCollectionNames()
[ "dispatches", "fm", "vehicles" ]
```

### **List all documents inside a collection**

Type the name of the collection in place of *collection*.

#### Definition
```
db.collection.find()
```
#### Example
To view everything inside the vehicles collection type: 
```
db.vehicles.find()
```
```
{ "_id" : ObjectId("5e701c2eb15e7c5673d3f0b3"), "vin" : "JNN2CMJARBD000556", "vehicle_name" : "AT-S025-BD000556", "vehicle_type" : "TRUCK", "vehicle_color" : "SEA_FORM_GREEN", "is_available" : true, "vehicle_position" : [ -97.73553, 30.26745 ], "vehicle_status" : "OK" }
{ "_id" : ObjectId("5e7bdb2a93b142e5c8f1c123"), "vin" : "JMLRWML30HC015174", "vehicle_name" : "AV-C206-HC015174", "vehicle_type" : "VAN", "vehicle_color" : "CAMO", "is_available" : true, "vehicle_position" : [ 0, 0 ], "vehicle_status" : "OK" }
```

To make it more readable append .pretty() at the end.

```
db.vehicles.find().pretty()
```
```
> db.vehicles.find().pretty()
{
        "_id" : ObjectId("5e701c2eb15e7c5673d3f0b3"),
        "vin" : "JNN2CMJARBD000556",
        "vehicle_name" : "AT-S025-BD000556",
        "vehicle_type" : "TRUCK",
        "vehicle_color" : "SEA_FORM_GREEN",
        "is_available" : true,
        "vehicle_position" : [
                -97.73553,
                30.26745
        ],
        "vehicle_status" : "OK"
}
{
        "_id" : ObjectId("5e7bdb2a93b142e5c8f1c123"),
        "vin" : "JMLRWML30HC015174",
        "vehicle_name" : "AV-C206-HC015174",
        "vehicle_type" : "VAN",
        "vehicle_color" : "CAMO",
        "is_available" : true,
        "vehicle_position" : [
                0,
                0
        ],
        "vehicle_status" : "OK"
}
```

### **Show documents based on a query**
A query filters documents in the collection to give you documents that contain the items in the query.

**Important TIP**: When querying with an id, ensure that you're using ObjectId and not a string as _id is stored as an ObjectId in the database. More on this in the **"Insert a document"** section.

#### Definition
```
// Projection is optional

db.collection.find(query, projection)
```
#### Example
```
// Searches for vehicles that has true in their "is_available" key.
// _id: 0 will suppress the id field and only return what is queried. By default the _id will be included in each find() call.

db.vehicles.find({"is_available": true}, {_id: 0})


// This will output the same as above but includes the _id key.

db.vehicles.find({"is_available": true})
```

### **Logging out**
You can press Ctrl+C to log out or just type:
```
quit()
```


## __Modifying MongoDB Commands__

### **Insert a document**

Insert a document by listing all the keys and values for it. 

#### Definition
```
db.collection.insert({query})
```
#### Example
```
db.vehicles.insert({"vin" : "test_VIN", "vehicle_name": "test_vehicleName", "vehicle_type": "test_vehicleType", "vehicle_color": "test_color", "is_available": true, "vehicle_position" : [0,0], "vehicle_status": "OK"})
```

A key called _id will be randomly generated upon insertion. This is not a string, it will be an object called ObjectId. In Python, convert this into a string before using it. If you are planning on querying with an id in Python, convert it first into an ObjectId if it's not already.
```
# Python
# Import ObjectId to convert the id from a string into ObjectId

from bson.objectid import ObjectId

# query_id is a string
query = {"_id": ObjectId(query_id)}
```

### **Update a document**
Updates a single document that is found using the query.

https://docs.mongodb.com/manual/reference/method/db.collection.update/

#### Definition
```
db.collection.update({query}, {new_values}, {optional_parameters})
```
This example updates multiple vehicle statuses from OK to AVAILABLE.

#### Example
```
db.vehicles.update({"vehicle_status":"OK"}, { $set: {"vehicle_status":"AVAILABLE"}}, { multi: true})
```

### **Remove a document**
Removes any document that is found using the query.

#### Definition
```
db.collection.remove({query})
```
#### Example
```
// Removes any vehicle with test_VIN inside their vin key.

db.vehicles.remove({"vin":"test_VIN"})
```

### **Remove all documents in a collection**
An empty query will delete all the documents in the collection. Don't do this unless you are certain you want to clear the collection.

#### Definition
```
db.collection.remove({})
```

#### Example
```
db.vehicles.remove({})
```