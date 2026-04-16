import time
import random
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8080/api/sensor-update")

zones = {
    "ZONE_ENTRANCE": {"id": "ZONE_ENTRANCE", "name": "North Gate Entrance", "currentCount": 0, "capacity": 500, "safetyStatus": "GREEN"},
    "ZONE_STAND_A": {"id": "ZONE_STAND_A", "name": "East Stand A", "currentCount": 0, "capacity": 2000, "safetyStatus": "GREEN"},
    "ZONE_STAND_B": {"id": "ZONE_STAND_B", "name": "West Stand B", "currentCount": 0, "capacity": 1500, "safetyStatus": "GREEN"},
    "ZONE_CONCOURSE": {"id": "ZONE_CONCOURSE", "name": "Main Concourse", "currentCount": 0, "capacity": 1000, "safetyStatus": "GREEN"}
}

def send_update(zone_id):
    zone_data = zones[zone_id]
    try:
        response = requests.post(API_URL, json=zone_data, timeout=2)
        if response.status_code == 200:
            print(f"Pushed update for {zone_id}: {zone_data['currentCount']}/{zone_data['capacity']}")
    except Exception as e:
        print(f"Failed to send update for {zone_id}: {e}")

def run_simulation():
    print("Starting stadium simulation...")
    tick = 0
    while True:
        tick += 1
        print(f"\n--- Simulation Tick {tick} ---")
        
        # Simulate people arriving at the entrance
        if tick < 50:
            arrival_rate = random.randint(20, 100)
            zones["ZONE_ENTRANCE"]["currentCount"] = min(zones["ZONE_ENTRANCE"]["capacity"], zones["ZONE_ENTRANCE"]["currentCount"] + arrival_rate)
            
        # Simulate people moving from entrance to concourse
        if tick > 5 and zones["ZONE_ENTRANCE"]["currentCount"] > 0:
            move_rate = min(zones["ZONE_ENTRANCE"]["currentCount"], random.randint(50, 150))
            zones["ZONE_ENTRANCE"]["currentCount"] -= move_rate
            zones["ZONE_CONCOURSE"]["currentCount"] = min(zones["ZONE_CONCOURSE"]["capacity"], zones["ZONE_CONCOURSE"]["currentCount"] + move_rate)
            
        # Simulate people moving from concourse to stands
        if tick > 10 and zones["ZONE_CONCOURSE"]["currentCount"] > 0:
            move_rate_a = min(zones["ZONE_CONCOURSE"]["currentCount"] // 2, random.randint(20, 80))
            zones["ZONE_CONCOURSE"]["currentCount"] -= move_rate_a
            zones["ZONE_STAND_A"]["currentCount"] = min(zones["ZONE_STAND_A"]["capacity"], zones["ZONE_STAND_A"]["currentCount"] + move_rate_a)
            
            move_rate_b = min(zones["ZONE_CONCOURSE"]["currentCount"], random.randint(20, 80))
            zones["ZONE_CONCOURSE"]["currentCount"] -= move_rate_b
            zones["ZONE_STAND_B"]["currentCount"] = min(zones["ZONE_STAND_B"]["capacity"], zones["ZONE_STAND_B"]["currentCount"] + move_rate_b)

        # People start to leave late in the game
        if tick > 100:
            for zone_id in ["ZONE_STAND_A", "ZONE_STAND_B", "ZONE_CONCOURSE", "ZONE_ENTRANCE"]:
                leave_rate = min(zones[zone_id]["currentCount"], random.randint(10, 50))
                zones[zone_id]["currentCount"] -= leave_rate
                
        # Send updates for all zones
        for zone_id in zones:
            send_update(zone_id)
            
        time.sleep(3)

if __name__ == "__main__":
    # Wait for the backend to be ready
    print("Waiting for backend to be ready...")
    time.sleep(15)
    run_simulation()
