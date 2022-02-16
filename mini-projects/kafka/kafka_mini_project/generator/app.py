# generator/app.py
import os
from time import sleep
from kafka import KafkaProducer
from transactions import create_random_transaction

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
    while True:
        transaction: dict = create_random_transaction()
        message: str = json.dumps(transaction)
        producer.send("queueing.transactions", value=message.encode())
        sleep(1)