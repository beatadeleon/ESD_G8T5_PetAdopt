#!/usr/bin/env python3
import amqp_connection
import pika
from os import environ
from send_email import send_email

hostname = environ.get('rabbit_host') #localhost
port = environ.get('rabbit_port')         #5672 

queue_names = ['open', 'pending', 'accept', 'reject', 'cancel']

def receiveNotif(channel):
    try:
        for queue_name in queue_names:
            print(f'{queue_name}: Consuming from queue:', queue_name)
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print('Waiting for messages. To exit, press CTRL+C')
        channel.start_consuming()

    
    
    except pika.exceptions.AMQPError as e:
        print(f"accept: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("accept: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an email by " + __file__)
    subject, receiver_email, message = body.decode().split(',')
    send_email(receiver_email, subject, message)

    

if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("notifications microservice: Getting Connection")
    connection = amqp_connection.create_connection(hostname, port, max_retries=12, retry_interval=5) #get the connection to the broker
    print("notifications microservice: Connection established successfully")
    channel = connection.channel()
    receiveNotif(channel)
