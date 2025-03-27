import requests
import time
import os
import random
from flask import Flask, jsonify, request
import threading
from werkzeug.exceptions import HTTPException

HOST = '0.0.0.0'
PORT = 8000
MODULE_NAME = os.getenv('MODULE_NAME')
app = Flask(__name__)


@app.route('/confirm_route', methods=['POST'])
def confirm_route():
    try:
        print(f"[{MODULE_NAME}] receive route to confirm")
        if (random.randint(0 , 3) >= 1):
            print("Route confirmed")
            return jsonify({"confirm": "YES"}) , 200
        else:
            return jsonify({"confirm": "NO"}) , 200
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error getting route: {e}")
    return jsonify({"status": "NO RESULT"})

@app.route('/current_coordinates', methods = ['POST'])
def current_coordinates():
    try:
        print(f"[{MODULE_NAME}] receive current coordinates")
        return jsonify({"status": "OK , keep moving"}) , 200
    except requests.RequestException as e:
        print(f"[{MODULE_NAME}] Error getting route: {e}")
    return jsonify({"status": "NO RESULT"})

def start_web():
    threading.Thread(target=lambda: app.run(
        host=HOST, port=PORT, debug=True, use_reloader=False
    )).start()