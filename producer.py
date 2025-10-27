import time
import json
import random
from Kafka import KafkaProducer
webpages = ['/home', '/products', '/about', '/contact', '/checkout']
print("Connecting to Kafka...")
producer = None
for _ in range(10): # Retry 10 times
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:29092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka!")
        break
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}. Retrying in 5s...")
        time.sleep(5)

if not producer:
    raise Exception("Could not connect to Kafka after retries.")

# Start sending fake click data
print("Sending click data...")
while True:
    click_data = {
        'user_id': f'user_{random.randint(1, 100)}',
        'page': random.choice(webpages),
        'timestamp': time.time()
    }
    
    producer.send('clicks', value=click_data)
    print(f"Sent: {click_data}")
    
    time.sleep(random.uniform(0.1, 1.0)) # Send 1-10 events per second
