import pika
import json

# todo: add RabbitMQ messaging queuing

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order notify")
queue_name = queue.method.queue

channel.queue_bind(
    exchange="order",

)