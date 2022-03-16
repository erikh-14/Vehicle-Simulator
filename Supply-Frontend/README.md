# Supply-Frontend #

## Project Description 

WeGo's mission: create unique, high-value, first-of-a-kind software applications for the Transportation Industry.

WeGo's project based approach: leverage creative small teams and the agile scrum framework to trail blaze emerging customer business targets.

WeGo's tagline: get IT done good, fast and cheap .... WeGo wherever we gotta go to please each and every customer!

## Description

Displays a static html and css Fleet Manager login and fleet registration. You can register or generate a vehicle. There's a page shows all the vehicles from the database.

Within the code there is javascript which communicates with python using POST requests

### JSON objects

Login - Username, and Password

Registration - Fleet Name

### Requirements

```
1. HTML
4. CSS
2. Javascript
3. JSON
```

## Running the tests

Install Python 3.8 and Selenium.
Download Chrome Web Driver and move it to "C:\".

Run selenium_supply_login.py

## What are the folders and what do they contain?

css - Contains all of styling for supply
```
DashboardStyle.css
directoryStyle.css
dispatchStyle.css
fleet.jpg
fonts.css
loginPageFM.css
regVehicleStyle.css
supply.css
```
images - Contains all the images for supply
```
bus_1f68c.png
button_car.png
car.png
```
js - Contains all the javascript files for supply
```
display_vehicle.js
displayVechileOntoMap.js 
register_vehicle.js
```

## What does each file do?
```
dashboard.html - Landing page once logged in.
dispatch_record.html - Displays the records for dispatch
register_fleet.html - Registering page for fleet
register_vehicle.html - Registering page for vehicle 
vehicle_directory.html - Where vehicles are displayed
index.html - Login page for fleetmanager
vehicle_map.html - The map to load on the vehicles
vehicle_simulator_map.html - File simulates the vehicles
vehicle_status.html - File contains status of vehicles
```


### UI Style Guidelines

```
Submit Buttons
-	Color: #4caf50
-	TextColor: #ffffff
-	TextFont: Default
“Home” Buttons
-	Color: #f44336
-	TextColor: #ffffff
-	TextFont: Default
Other Buttons
-	Color: #03b9f5
-	TextColor: TextColor: #ffffff
-	TextFont: Default
Body Text
-	Color: #000000
-	Font: Default
-	Size: Dependent on Information
Main Background
-	Color: #26a8ff
Sub-background
-	Color: #baf3ff
Sub-title box (if needed)
-	Color: #79e8ff
```

## Built With

* HTML
* JavaScript
* CSS

## Authors

* **Will Luong** - *Map Services* 
* **Jeffrey Quade** - *Dev Ops, Tester* 
* **Colby Tang** - *Critical Path Developer, Backend Developer for Supply/Demand*
* **Erik Hernandez** - *Full Stack Supply* 
* **Hudson Smoot** - *Full Stack Demand* 
