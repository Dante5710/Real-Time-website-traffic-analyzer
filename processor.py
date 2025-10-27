import time
import json
from kafka import KafkaConsumer
import redis

print("Waiting for Kafka and Redis to start...")
time.sleep(15) # Simple way to wait for other services

# Connect to Kafka
consumer = KafkaConsumer(
    'clicks',
    bootstrap_servers='kafka:29092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)

print("Processor is running...")
for message in consumer:
    try:
        data = message.value
        page = data.get('page')
        
        if page:
            # Increment the count for this page in Redis
            # 'HINCRBY' increments a hash field (page_counts)
            # by a given value (1)
            r.hincrby('page_counts', page, 1)
            
            # Also, log the latest 100 events
            r.lpush('latest_events', json.dumps(data))
            r.ltrim('latest_events', 0, 99)
            
            print(f"Processed click for: {page}")
            
    except Exception as e:
        print(f"Error processing message: {e}")
