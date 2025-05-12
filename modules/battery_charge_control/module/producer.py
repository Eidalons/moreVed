import os
import json
import threading
import multiprocessing

from confluent_kafka import Producer
from random import randint
from time import sleep
from uuid import uuid4

_requests_queue: multiprocessing.Queue = None
MODULE_NAME = os.getenv("MODULE_NAME")

current_health = 100

def immitate_battery():
    global current_health
    """ Имитирует поведение АКБ. """
    while current_health > 0:
        proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "route-control",
            "operation": "set_battery",
            "health": current_health
        })
        current_health -= randint(3,5)
        sleep(35)

    proceed_to_deliver(uuid4().__str__(), {
            "deliver_to": "route-control",
            "operation": "set_battery",
            "health": 0
        })

def proceed_to_deliver(id, details):
    details["source"] = MODULE_NAME
    details["id"] = id
    _requests_queue.put(details)


def producer_job(_, config, requests_queue: multiprocessing.Queue):
    producer = Producer(config)

    threading.Thread(target=immitate_battery).start()

    def delivery_callback(err, msg):
        if err:
            print("[error] Message failed delivery: {}".format(err))

    topic = "monitor"
    while True:
        event_details = requests_queue.get()
        producer.produce(
            topic,
            json.dumps(event_details),
            event_details["id"],
            callback=delivery_callback
        )

        producer.poll(10000)
        producer.flush()


def start_producer(args, config, requests_queue):
    print(f"{MODULE_NAME}_producer started")

    global _requests_queue

    _requests_queue = requests_queue
    threading.Thread(
        target=lambda: producer_job(args, config, requests_queue)
    ).start()