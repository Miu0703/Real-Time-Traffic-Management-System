# producer.py
from kafka import KafkaProducer
import json
import time
import random

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate traffic data
def generate_traffic_data():
    data = {
        'timestamp': time.time(),
        'location': f'Location_{random.randint(1, 100)}',
        'traffic_level': random.randint(1, 10)  # 1: Low, 10: High
    }
    return data

if __name__ == "__main__":
    while True:
        traffic_data = generate_traffic_data()
        producer.send('traffic-data', traffic_data)
        print(f"Produced: {traffic_data}")
        time.sleep(1)  # Send data every second
