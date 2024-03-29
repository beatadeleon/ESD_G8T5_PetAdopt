import pika
from pika.exceptions import AMQPConnectionError
import os

exchangename = "notifications" 
exchangetype = "topic" 

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
    
    else:
        subject = 'Sorry to see you go!'
        message = f"Hi {name}. This is to confirm that you have cancelled your request for {pet}."

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
        
        body = f"{subject}, {email}, {message}"
        channel.basic_publish(exchange=exchangename, routing_key=email + f'.{status}', 
                               body=body, properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
        
        return {'status': 201, 'message': f'{status} email sent successfully'}
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)
