import os
import json
import threading

from uuid import uuid4
from time import sleep
from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")


def set_route(route):
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "movement-calculation",
            "operation": "set_route",
            "route": route
        })
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "route-control",
            "operation": "set_route",
            "route": route
        })
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "task-execution-control",
            "operation": "set_task",
            "task": route[2] # добавить нормальное задание
        })

def send_telemetry(telemetry):
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "crypto",
            "operation": "send_telemetry",
            "telemetry": telemetry 
        })
    print("[MESSAGE PROCCESING] send telemetry to crypto")

def send_emergency_external():
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "emergency-stop",
            "operation": "emergency_stop",
        })
    print("[MESSAGE PROCCESING] send request to stop boat")

def send_emergency_internal(code):
    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "crypto",
            "operation": "emergency-stop",
            "code": code
        })
    print("[MESSAGE PROCCESING] send msg about emergency")


def handle_event(id, details_str):
    """ Модуль сбора данных. """
    details = json.loads(details_str)
    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")
    

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")


    if operation == "route_complete":
        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "crypto",
            "operation": "route_complete"
        })

    if operation == "send_telemetry":
        telemetry = details.get("telemetry")
        send_telemetry(telemetry)
        print("[message_processing] get telemetry")

    if operation == "set_route":
        route = details.get("route")
        print("[message processing] accepted new route and task!")
        set_route(route)

    if operation == "emergency_stop" and source == "crypto":
        print("[message processing] request to stop the boat by emergency")
        send_emergency_external()
    if operation == "emergency_stop" and source == "emergency-stop":
        code = details.get("code")
        send_emergency_internal(code)
        print("[message processing] boat stopped by internal emergency system")
        

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

