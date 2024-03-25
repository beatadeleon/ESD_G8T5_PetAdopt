from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import pika
from pika.exceptions import AMQPConnectionError
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

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


adoption_URL = "http://localhost:5110/adoptionRequests/{}"
# accept_URL = "http://localhost:5200/accept"
# shortlisted_URL = "http://localhost:5200/shortlist"
# rejected_URL = "http://localhost:5200/reject"




@app.route("/accept_request", methods=['POST'])
def accept_request():
    if request.is_json:
        try:
            # Request is from adminDashboard. Data is in the form of {"application": ..., "status": ...}
            request_data = request.get_json()
            print("\nReceived a request in JSON:", request_data)
            
            # Get the application data
            application_data = request_data["application"]
            print("\n Application data in JSON:", application_data)
            
            # Get the new status data
            new_status = request_data["status"]
            print("\n New status data in JSON:", new_status)

            # Update adoption status
            adoption_response =invoke_http(adoption_URL.format(application_data.get('requestId')), method='PUT', json={"status": new_status})
            print('Adoption response:', adoption_response)

            # Determine the notification URL based on the adoption status
            if new_status == 'pending' or new_status == 'rejected' or new_status == 'confirmed':
                notification_response = send_notifications(application_data, new_status)
                print('Notification response:', notification_response)
            else:
                return jsonify({
                    "code": 400,
                    "message": f"Invalid status: {new_status}"
                }), 400

            

            return jsonify({
                "adoption_response": adoption_response,
                "notification_response": notification_response
            }), 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Accept request microservice internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def send_notifications(application_data, status):
    email = application_data['email']
    name = application_data['name']
    pet = application_data['pet']
    if status == 'pending':
        subject = "You're shortlisted!"
        message = f"Hi {name}. You're shortlisted to visit {pet}. Please book an appointment for us to assess your suitability"
    elif status == 'confirmed':
        subject = "Good news! You're accepted!"
        message = f"Hi {name}. Your application is successful. Please come down to pick up {pet}"    
    else:
        subject = "Adoption request update"
        message = f"Hi {name}. Your application for {pet} is unsuccessful. Thanks for your interest and you may apply for more pets"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.confirm', 
                            body=body, properties=pika.BasicProperties(delivery_mode=2))
        return {'status':201, 'message': 'Confirmation email sent successfully'}
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)    

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for accepting adoption requests...")
    app.run(host="0.0.0.0", port=5400, debug=True)