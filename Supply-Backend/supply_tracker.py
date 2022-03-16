# Heartbeat Tracker
# Keeps track of each vehicle's heartbeat report and checks if there are any missed heartbeats.

import supply_database_utils

import time

try:
    tracker_active = True
    db = supply_database_utils.Supply_Database_Utils()
    
    while tracker_active:
        print ("tracking")
        all_vehicles = db.get_all_vehicles()
        time.sleep(3)
except KeyboardInterrupt:
    tracker_active = False
    print ("Tracker stopped!")