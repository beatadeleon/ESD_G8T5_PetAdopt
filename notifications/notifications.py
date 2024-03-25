from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from pika.exceptions import AMQPConnectionError
import sys

app = Flask(__name__)
CORS(app, supports_credentials=True)

exchangename = "test_email" # exchange name
exchangetype = "topic" # use a 'topic' exchange to enable interaction

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
except AMQPConnectionError as e:
    print("Failed to establish connection to RabbitMQ:", str(e))
    sys.exit(1)
    
# SEND CONFIRMATION EMAIL  
@app.route('/confirm', methods=['POST'])
def confirm():
    email = request.get_json()['email']
    name = request.get_json()['name']
    pet = request.get_json()['pet']
    subject = 'Confirmation of adoption request'
    # Need to change to name of user, might need to retrieve from db
    message = f"Hi {name}. This email is to confirm your adoption request for {pet}. Please track your application regularly on the website"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.confirm', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({'status': 201, 'msg': 'CONFIRM NOTIFICATION SENT SUCCESSFULLY'}), 201
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)

# SEND SHORTLIST EMAIL   
@app.route('/shortlist', methods=['POST'])
def shortlist():
    email = request.get_json()['email']
    name = request.get_json()['name']
    pet = request.get_json()['pet']
    subject = "You're shortlisted!"
    message = f"Hi {name}. You're shortlisted to visit {pet}. Please book an appointment for us to assess your suitability"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.shortlist', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({'status': 201, 'msg': 'SHORTLIST NOTIFICATION SENT SUCCESSFULLY'}), 201
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)

# SEND ACCEPT EMAIL   
@app.route('/accept', methods=['POST'])
def accept():
    email = request.get_json()['email']
    name = request.get_json()['name']
    pet = request.get_json()['pet']
    subject = "Good news! You're accepted!"
    message = f"Hi {name}. Your application is successful. Please come down to pick up {pet}"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.accept', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({'status': 201, 'msg': 'ACCEPT NOTIFICATION SENT SUCCESSFULLY'}), 201
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)

# SEND REJECT EMAIL
@app.route('/reject', methods=['POST'])
def reject():
    try:
        for application in request.get_json():
            email = application['email']
            name = application['name']
            pet = application['pet']
            subject = "Adoption request update"
            message = f"Hi {name}. Your application for {pet} is unsuccessful. Thanks for your interest and you may apply for more pets"
            body = f"{subject}, {email}, {message}"
            channel.basic_publish(exchange=exchangename, routing_key=email+'.reject', 
                                body=body, properties=pika.BasicProperties(delivery_mode=2))      
        return jsonify({'status': 201, 'msg': 'REJECT NOTIFICATIONS SENT'}), 201
    except AMQPConnectionError as e:
        return "Failed to publish reject message due to connection error", str(e)
    except Exception as e:
        return jsonify({"status": 500, "message": "Failed to send rejection notifications and update applications"}), 500

# SEND CANCEL EMAIL
@app.route('/cancel', methods=['POST'])
def cancel():
    email = request.get_json()['email']
    name = request.get_json()['name']
    pet = request.get_json()['pet']
    subject = "Adoption request update"
    message = f"Hi {name}. Your application for {pet} has been succesfully cancelled. Thanks for your interest and you may apply for more pets"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.cancel', 
                              body=body, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({'status': 201, 'msg': 'CANCEL NOTIFICATION SENT SUCCESSFULLY'}), 201
    except AMQPConnectionError as e:
        return "Failed to publish cancel message due to connection error", str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)