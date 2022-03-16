# Supply-Backend #

# Project Description #

WeGo's mission: create unique, high-value, first-of-a-kind software applications for the Transportation Industry.

WeGo's project based approach: leverage creative small teams and the agile scrum framework to trail blaze emerging customer business targets.

WeGo's tagline: get IT done good, fast and cheap .... WeGo wherever we gotta go to please each and every customer!

### Requirements

```
1. Python
2. MongoDB
3. PyMongo
4. Nginx
5. Python Requests
```

## Running the tests

Postman API Calls: https://documenter.getpostman.com/view/10802260/SzYgRF9T?version=latest

### Coding Guidelines

None

## Built With

* Python

## What are the folders and what do they contain?
supply-test-cases - Contains all the test cases for the supply back end of the website
```
README - Copy.md                                
mapping_services_test_case,py               unit test cases to test for the server API request to the Mapbox geocoding API
selenium_supply_login.py                    Black box test using selenium to test for the supply server login. 
test_vehicle_generator.py                   unit testing for the supply server vehicle generator functionality of the website
unit_test_dispatch.py                       unit testing for the dispatch 
vehicle_unit_test.py                        unit testing for the vehicle such as testing for its position, vin, id generator. 
```

Main files in the Supply BE server: 
```
HeartbeatListener.py --> This python file mainly deals with detecting oncoming heartbeat package sent from the vehicle simulator
SupplyWebServer.py   --> This python file is the backbone of the Supply BE as it deals and handles the GET and POST request from different sources and response to those request. 
email_fm.py         -->  This file test the supply server ability to send a notificaiton to the FM via email. 
mapping_services.py  --> This python file will takes in addresses, stops from dispatch convert them into coordinate using Mapbox reverse geocoding API.
supply_api_heartbeat.py  --> This file will take the heartbeat sent from the vehicle simulator and update the database accordingly.
supply_api_vehicle.py  --> This file will make a vehicle object to handle registering, generating, removing a vehicles from the database. In addition, it also returns ETA between two addresses from mapbox and determining which vehicles is closest to an order. 
supply_database_utils.py   -> A utils python file that makes a connection to the mongoDB for the supply server to store and process data.
supply_dispatch.py          -> This python function create a dispatch.
supply_fleet.py             -> This function create a Fleet object that stores warehouese in the database. The fleet objects include: name, region, id, size and vehicle. 
suplpy_mongodb.md       -->Extensive readme documeentation mainly for Mongodb database.
supply_vehicle.py       --> This file create a vehicle class and assign attributes such as vehicle_id, vin number, name, etc, into it.
vin_generator.py            -->This will generate a vin number for a vehicle.
supply_tracker.py       --> Keeps track of each vehicle's heartbeat report and checks if there are any missed heartbeats.


```

## Authors

* **Will Luong** - *Map Services* 
* **Jeffrey Quade** - *Dev Opps* 
* **Colby Tang** - *Scrum Master* 
* **Erik Hernandez** - *Full Stack Supply* 
* **Hudson Smoot** - *Full Stack Demand* 
