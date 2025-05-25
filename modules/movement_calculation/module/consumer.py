import os
import json
import threading
from time import sleep
from random import randint
from uuid import uuid4
from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")

current_route = []

def move_move(route):
    global current_route
    current_route = route
    for point in range(0 , len(route) - 1):
        proceed_to_deliver(uuid4().__str__(), {
                "deliver_to": "movement-control",
                "operation": "move_to", 
                "current_point": route[point],
                "next_point": route[point + 1],
                "instructions":[randint(0, 180) , randint(-10 , 10)] 
            })
        print(f"calculate instruction to point number {point} of  ")
        sleep(7)


def handle_event(id, details_str):
    """ Модуль сбора данных. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "set_route":
        route = details.get("route")
        print("[movement calculation] get new route. Start calculating....")
        move_move(route)
        
        


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