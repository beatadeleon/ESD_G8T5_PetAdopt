import pika
from pika.exceptions import AMQPConnectionError
import os, sys

exchangename = "notifications" 
exchangetype="topic" 
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
except AMQPConnectionError as e:
    print("Failed to establish connection to RabbitMQ:", str(e))
    sys.exit(1)
    

def send_notifications(application_data, status):    
    email = application_data['email']
    name = application_data['name']
    pet = application_data['pet']
    
    if status == 'open':
        subject = 'Confirmation of adoption request'
        message = f"Hi {name}. This email is to confirm your adoption request for {pet}. Please track your application regularly on the website"
        
    elif status == 'pending':
        subject = "You're shortlisted!"
        message = f"Hi {name}. You're shortlisted to visit {pet}. Please book an appointment for us to assess your suitability"
        
    elif status == 'accept':
        subject = "Good news! You're accepted!"
        message = f"Hi {name}. Your application is successful. Please come down to pick up {pet}" 
           
    elif status == 'reject':
        subject = "Adoption request update"
        message = f"Hi {name}. Your application for {pet} is unsuccessful. Thanks for your interest and you may apply for more pets"
    # else:
        
    
    # Reject: batch processing
    body = f"{subject}, {email}, {message}"
    
    # Retry logic
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            channel.basic_publish(exchange=exchangename, routing_key=email+f'.{status}', 
                                body=body, properties=pika.BasicProperties(delivery_mode=2))
            return {'status':201, 'message': f'{status} email sent successfully after {attempt} attempts'}
        except AMQPConnectionError as e:
            print(f"Attempt {attempt}: Failed to publish {status} message due to connection error")
            if attempt == max_retries:
                return "Failed to publish message after maximum retry attempts", str(e)
    
    