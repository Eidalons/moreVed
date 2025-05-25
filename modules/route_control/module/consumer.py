import os
import json
import threading

from time import sleep
from random import randint
from uuid import uuid4
from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")

battery_health: int = 0
current_route = []
task = []
next_point = []
current_coords = []
epsilon = 10000
emergensy_flag = False

def set_battery(health):
    global battery_health
    battery_health = health
    if battery_health <= 0:
        if emergensy_flag:
            proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "emergency-stop",
            "operation": "emergency_stop",
            "code": 3
        })
        pass
    print(f"[ROUTE CONTROL] current battery health =\t{battery_health}")


def validate_movement(point):
    global current_route, next_point
    if (point[0] == current_route[len(current_route) - 1][0]) and (point[1] == current_route[len(current_route) - 1][1]):
        sleep(10)
        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "message-processing",
            "operation": "route_complete",
        })
    if point in current_route:
        print("[ROUTE CONTROL] movement_confirmed!")
    else:
        if emergensy_flag:
            proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "emergency-stop",
            "operation": "emergency_stop",
            "code": 2
        })


def set_route(route):
    global current_route
    current_route = route

def validate_coords(coords):
    global next_point
    if (abs(next_point[0] - coords[0]) < epsilon) and (abs(next_point[1] - coords[1]) < epsilon):
        print("[ROUTE CONTROL] current coords are not a deviation the route")
    else:
        if emergensy_flag:
            proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "emergency-stop",
            "operation": "emergency_stop",
            "code": 1
        })

def handle_event(id, details_str):
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "set_battery":
        health = details.get("health")
        set_battery(health)

    if operation == "move_to":
        next_point = details.get("next_point")
        validate_movement(next_point)

    if operation == "set_route":
        route = details.get("route")
        set_route(route)
        print("[ROUTE CONTROL] set up new route")

    if operation == "set_coords":
        coords = details.get("coords")
        current_coords = coords
        if len(current_route) != 0:
            validate_coords(current_coords)

    


    


def consumer_job(args, config):
    consumer = Consumer(config)

    def reset_offset(verifier_consumer, partitions):
        if not args.reset:
            return

        for p in partitions:
            p.offset = OFFSET_BEGINNING
        verifier_consumer.assign(partitions)

    topic = MODULE_NAME
    consumer.subscribe([topic], on_assign=reset_offset)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    handle_event(id, details_str)
                except Exception as e:
                    print(f"[error] Malformed event received from " \
                          f"topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

def start_consumer(args, config):
    print(f'{MODULE_NAME}_consumer started')
    threading.Thread(target=lambda: consumer_job(args, config)).start()