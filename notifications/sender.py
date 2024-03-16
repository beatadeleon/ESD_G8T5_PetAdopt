from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from pika.exceptions import AMQPConnectionError
import sys

app = Flask(__name__)
CORS(app, supports_credentials=True)

exchangename = "test_email" # exchange name
exchangetype = "topic" # use a 'topic' exchange to enable interaction

# Create a connection and a channel to the broker to publish messages to activity_log, error queues
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
except AMQPConnectionError as e:
    print("Failed to establish connection to RabbitMQ:", str(e))
    sys.exit(1)
    
    
@app.route('/confirm', methods=['POST'])
def confirm():
    email = request.get_json()['email']
    subject = 'Confirmation of adoption request'
    message = f"Hi ${email}. This email is to confirm your adoption request"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.confirm', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "{'status': 201, 'msg': 'CONFIRM NOTIFICATION SENT SUCCESSFULLY'}"
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)
    
@app.route('/shortlist', methods=['POST'])
def shortlist():
    email = request.get_json()['email']
    subject = "You're shortlisted!"
    message = f"Hi ${email}. You're shortlisted to visit Pet XXXX. Please book an appointment for us to assess your suitability"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.shortlist', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "{'status': 201, 'msg': 'SHORTLIST NOTIFICATION SENT SUCCESSFULLY'}"
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)
    
@app.route('/accept', methods=['POST'])
def accept():
    email = request.get_json()['email']
    subject = "Good news! You're accepted!"
    message = f"Hi ${email}. Your application is successful. Please come down to pick up Pet XXXX"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.accept', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "{'status': 201, 'msg': 'ACCEPT NOTIFICATION SENT SUCCESSFULLY'}"
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)

@app.route('/reject', methods=['POST'])
def reject():
    email = request.get_json()['email']
    subject = "Adoption request update"
    message = f"Hi ${email}. Your application is unsuccessful. Thanks for your interest and you may apply for more pets"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.reject', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "{'status': 201, 'msg': 'REJECT NOTIFICATION SENT SUCCESSFULLY'}"
    except AMQPConnectionError as e:
        return "Failed to publish reject message due to connection error", str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)