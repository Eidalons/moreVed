import time
import threading
import random
import os
import json

from uuid import uuid4
from time import sleep
from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver


MODULE_NAME = os.getenv("MODULE_NAME")
COORDS_PATH: str = "/shared/coords"



def read_coords():
    """ Получает данные навигационной системы. """
    with open(COORDS_PATH, "a+") as file:
        pass

    with open(COORDS_PATH, "r") as file:
        coords = file.read().strip().split(",")

    if not coords or len(coords) != 2:
        return [0, 0]

    try:
        coords = list(map(int, coords))
    except:
        return [0, 0]

    return coords

def check_route(route):
    print("[CRYPTO] route confirmed!")
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "message-processing",
            "operation": "set_route",
            "route": route
        })

def send_telemetry(telemetry):
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "communication",
            "operation": "send_telemetry",
            "telemetry": telemetry 
        })
    print("[CRYPTO] send telemetry to crypto")

def send_emergency_external():
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "message-processing",
            "operation": "emergency_stop",
        })
    print("[CRYPTO] send emergency stop signal")

def send_emergency_internal(code):
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "communication",
            "operation": "emergency_stop",
            "code":code
        })
    print("[CRYPTO] send info about boat stop")


def encrypt_message(message):
    #add hash
    print("[CRYPTO] message encrypted")
    pass


def handle_event(id, details_str):
    """ Обработчик входящих в модуль задач. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    #data: str = details.get("data")
    operation: str = details.get("operation")

    if operation == "set_route":
        route = details.get("route")
        print("[CRYTO] accepted new possible route , checking ......")
        check_route(route)

    if operation == "send_telemetry":
        telemetry = details.get("telemetry")
        encrypt_message(telemetry)
        send_telemetry(telemetry)
        print("[CRYPTO] send encrypted telemetry to communication")

    if operation == "emergency_stop" and source == "communication":
        encrypt_message(source) #######
        send_emergency_external()
        print(["[CRYPTO] accepted commant to stop by emergency"])

    if operation == "emergency_stop" and source == "message-processing":
        encrypt_message(source) ######
        code = details.get("code")
        send_emergency_internal(code)
        print(["[CRYPTO] accepted commant to stop by emergency"])

    if operation == "route_complete":
        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "communication",
            "operation": "route_complete"
        })

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")
    

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
                    id = msg.key().decode("utf-8")
                    details_str = msg.value().decode("utf-8")
                    handle_event(id, details_str)
                except Exception as e:
                    print(f"[error] Malformed event received from " \
                          f"topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

def start_consumer(args, config):
    print(f"{MODULE_NAME}_consumer started")
    threading.Thread(target=lambda: consumer_job(args, config)).start()