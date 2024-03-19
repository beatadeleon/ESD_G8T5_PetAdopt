#!/usr/bin/env python3
import amqp_connection
import json
import pika
#from os import environ
from test_email import send_email


confirm_queue_name = 'confirm' 
s_queue_name = 'shortlist' 
a_queue_name = 'accept' 
r_queue_name = 'reject' 
cancel_queue_name = 'cancel' 


def receiveOrderLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        print('accept: Consuming from queue:', a_queue_name)
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('shortlist: Consuming from queue:', s_queue_name)
        channel.basic_consume(queue=s_queue_name, on_message_callback=callback, auto_ack=True)
        print('confirm: Consuming from queue:', confirm_queue_name)
        channel.basic_consume(queue=confirm_queue_name, on_message_callback=callback, auto_ack=True)
        print('reject: Consuming from queue:', r_queue_name)
        channel.basic_consume(queue=r_queue_name, on_message_callback=callback, auto_ack=True)
        print('reject: Consuming from queue:', cancel_queue_name)
        channel.basic_consume(queue=cancel_queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    
    except pika.exceptions.AMQPError as e:
        print(f"accept: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("accept: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\naccept: Received an order log by " + __file__)
    subject, receiver_email, message = body.decode().split(',')
    send_email(receiver_email, subject, message)

    



connection = amqp_connection.create_connection()  # get the connection to the broker
channel = connection.channel()
receiveOrderLog(channel)
