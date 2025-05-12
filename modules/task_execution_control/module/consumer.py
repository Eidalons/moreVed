import os
import json
import threading

from uuid import uuid4
from confluent_kafka import Consumer, OFFSET_BEGINNING
from .producer import proceed_to_deliver

MODULE_NAME: str = os.getenv("MODULE_NAME")

task = {
    "coords": [0,0]
}

def check_task(coords):
    if  coords[0] == task["coords"][0] and coords[1] == task["coords"][1]:
        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "sensors",
            "operation": "get_sample",
        })
    else:
        print("current coords aren't equal to task coords")
        pass
        

    
def set_task(task_coords):
    global task
    task["coords"][0] = task_coords[0]
    task["coords"][1] = task_coords[1]

def handle_event(id, details_str):
    """ Модуль сбора данных. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    operation: str = details.get("operation")
    

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "set_coords":
        print("[TASK_EXECUTION_CONTROL] get current coords")
        coords = details.get("coords")
        check_task(coords)
    
    if operation == "set_task":
        print("[TASK_EXECUTION_CONTROL] get new task")
        task_coords = details.get("task")
        set_task(task_coords)

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

