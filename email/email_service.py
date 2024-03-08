from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from pika.exceptions import AMQPConnectionError
import sys

app = Flask(__name__)
CORS(app)

exchangename = "test_email" # exchange name
exchangetype = "topic" # use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
# exchangename = environ.get('exchangename') #order_topic
# exchangetype = environ.get('exchangetype') #topic 

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
    data = request.get_json()
    email = data['email']
    subject = 'Confirmation of adoption request'
    message = data['message']
    body = f"{subject}, {email}, {message}"
    
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.confirm', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "Got the confirm message", data
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)
    
    
@app.route('/shortlist', methods=['POST'])
def shortlist():
    data = request.get_json()
    email = data['email']
    subject = 'Adoption request next steps'
    message = data['message']
    body = f"{subject}, {email}, {message}"
    
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.shortlist', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "Got the shortlist message", data
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)
    
@app.route('/accept', methods=['POST'])
def accept():
    data = request.get_json()
    email = data['email']
    subject = "Good news! You're accepted!"
    message = data['message']
    body = f"{subject}, {email}, {message}"
    
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.accept', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "Got the accept message", data
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)

@app.route('/reject', methods=['POST'])
def reject():
    data = request.get_json()
    email = data['email']
    subject = "Adoption request update"
    message = data['message']
    body = f"{subject}, {email}, {message}"
    
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.reject', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return "Got the reject message", data
    except AMQPConnectionError as e:
        return "Failed to publish reject message due to connection error", str(e)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
