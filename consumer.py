# consumer.py
from kafka import KafkaConsumer
import json

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'traffic-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='traffic-group',
    value_serializer=lambda v: json.loads(v.decode('utf-8'))
)

if __name__ == "__main__":
    for message in consumer:
        traffic_data = message.value
        print(f"Consumed: {traffic_data}")
