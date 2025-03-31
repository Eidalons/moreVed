import requests
import os
import time
import random
from flask import Flask, jsonify, request
import threading
from werkzeug.exceptions import HTTPException

HOST = '0.0.0.0'
PORT = 8000
MODULE_NAME = os.getenv('MODULE_NAME')
app = Flask(__name__)
boat_instance = None
current_route = None
#state = False
CKOB_URL = 'http://ckob:8000/receive_coordinates'
ORVD_URL = 'http://orvd:8000/current_coordinates'

class Point:
    def __init__(self ,x , y, uid):
        self.x = x
        self.y = y
        self.uid = uid
    
    def distance(self, second):
        steps = 5
        diff = [(second.x - self.x) / steps , (second.y - self.y) / steps]
        for i in range(steps - 1):
            self.x += diff[0]
            self.y += diff[1]
            time.sleep(1)
            print("Moving to next coordinate, current x , y " , self.x , "\t" , self.y)
        self.x = second.x
        self.y = second.y
        print("Moving to next coordinate, current x , y " , self.x , "\t" , self.y) 
        return self  

    def __repr__(self):
        return f"Point(uid={self.uid}, x={self.x}, y={self.y})"
    
class Boat:
    def __init__(self, route):
        self.starting_point = Point(0,0,0)
        self.current_point = Point(0,0,0)
        self.route = route
        self.sensors_data = []
        
    def start_moving(self):
        time.sleep(2)
        for i in range(len(current_route)):
            self.current_point.distance(self.route[i])
            record_sensors_data()
            send_informatoin_to_services()
            time.sleep(2)
        print("route_complete!")


@app.route('/start_route', methods=['POST'])
def start_route():
    global boat_instance
    global current_route
    try:
        print(f"[{MODULE_NAME}] receive route")
        response_data = request.get_json()
        route = list(response_data.get("route"))
        print("Полученный маршрут" , route)
        current_route = route
        transformed_route = transform_route(route)

        boat_instance = Boat(transformed_route)
        print("Create boat")
        threading.Thread(target=boat_instance.start_moving).start()
        print("Start moving!")
        return jsonify({"status": "route started"}) , 200
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error getting route: {e}")  
    return jsonify({"status": "NO RESULT"})



def transform_route(route):
    transformed_route = []
    for i in range(len(route)):
        transformed_route.append(Point(route[i][0], route[i][1], i))
    return transformed_route


def send_informatoin_to_services():
        global boat_instance
        try:
            print(f"[{MODULE_NAME}] send current coordinate to orvd")
            json_data_orvd = {"current_coordinates_x:":boat_instance.current_point.x, "current_coordinates_y":boat_instance.current_point.y}
            response_orvd = requests.post(ORVD_URL, json = json_data_orvd)

            json_data_ckob = {"current_coordinates_x":boat_instance.current_point.x, "current_coordinates_y":boat_instance.current_point.y, "sensors_data": boat_instance.sensors_data  }
            response_ckob = requests.post(CKOB_URL, json = json_data_ckob)

            response_data_orvd = response_orvd.json()
            response_data_ckob = response_ckob.json()
            print("ordv answer : " , response_data_orvd , "\t" , "ckob answer",response_data_ckob)

        except requests.RequestException as e:
            print(f"[{MODULE_NAME}] Error send route: {e}")

def record_sensors_data():
    global boat_instance
    radiation = random.randint(0, 4)
    ph = random.randint(0, 14)
    data = [ph , radiation]
    boat_instance.sensors_data.append(data)

def start_web():
    threading.Thread(target=lambda: app.run(
        host=HOST, port=PORT, debug=True, use_reloader=False
    )).start()