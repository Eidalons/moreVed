import requests
import time
import os
from flask import Flask, jsonify, request
import threading
import random
from werkzeug.exceptions import HTTPException

HOST = '0.0.0.0'
PORT = 8000
MODULE_NAME = os.getenv('MODULE_NAME')
app = Flask(__name__)

current_route = [[random.randint(1, 100), random.randint(1, 100)] for x in range(5)]
confirmation = False
BOAT_URL = 'http://boat:8000/start_route'
ORVD_URL = 'http://orvd:8000/confirm_route'

def send_route_to_orvd():
    global confirmation
    global current_route
    try:
        print(f"[{MODULE_NAME}] send route to orvd")
        json_data = {"route": current_route}
        response = requests.post(ORVD_URL, json = json_data)
        response_data = response.json()
        if (response_data.get("confirm") == "YES"):
            confirmation = True
            print("route confirmed!")
        else:
            print("route rejected , resend request with new route")
            confirmation = False
            current_route = [[random.randint(1, 100), random.randint(1, 100)] for x in range(5)]
            send_route_to_orvd()
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error send route: {e}")

def send_route_to_boat():
    global current_route
    global confirmation
    while (confirmation is False):
        time.sleep(1)
    try:
        print(f"[{MODULE_NAME}] send route to boat")
        json_data = {"route": current_route}
        response = requests.post(BOAT_URL, json = json_data)
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error send route: {e}")

@app.route('/receive_coordinates' , methods = ['POST'])
def receive_coordinates():
    try:
        print(f"[{MODULE_NAME}] receive current coordinates from boat")
        response_data = request.get_json()
        print(response_data)
        return jsonify({"status": "got coordinates and data from sensors"}) , 200
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error getting route: {e}")
    return jsonify({"status": "NO RESULT"})

def start_web():
    time.sleep(10)
    send_route_to_orvd()
    send_route_to_boat()
    threading.Thread(target=lambda: app.run(
        host=HOST, port=PORT, debug=True, use_reloader=False
    )).start()