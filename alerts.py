import pika
import json
from datetime import datetime
import time

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break
    except pika.exceptions.AMQPConnectionError:
        print("Czekam na RabbitMQ...")
        time.sleep(3)

channel = connection.channel()
channel.queue_declare(queue='temperature_data')

def callback(ch, method, properties, body):
    data = json.loads(body)
    temp = data['temp']
    sensor_id = data['sensor_id']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if temp > 25.0:
        alert_msg = f"[{now}] ALARM! Sensor: {sensor_id}, Temp: {temp}C"
        print(f" !!! {alert_msg}")
        
        with open("alerts_history.txt", "a") as file:
            file.write(alert_msg + "\n")
    else:
        print(f" [{now}] Norma: {temp}C")

channel.basic_consume(queue='temperature_data', on_message_callback=callback, auto_ack=True)

print('--- System Alarmowy uruchomiony (zapisuje historię do pliku) ---')
channel.start_consuming()