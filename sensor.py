import pika
import time
import random
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='temperature_data')

print("--- Sensor uruchomiony. Wysyłam dane... ---")

try:
    while True:
        temp = round(random.uniform(18.0, 30.0), 2)
        message = json.dumps({"sensor_id": "Room_A", "temp": temp})
        
        channel.basic_publish(exchange='', routing_key='temperature_data', body=message)
        print(f" [x] Wysłano: {message}")
        
        time.sleep(2)  
except KeyboardInterrupt:
    connection.close()