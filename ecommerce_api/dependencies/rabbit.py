import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order notify")
queue_name = queue.method.queue

channel.queue_bind(
    exchange="order",

)