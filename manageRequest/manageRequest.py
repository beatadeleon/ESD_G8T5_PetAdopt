from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from pika.exceptions import AMQPConnectionError
import os, sys
import requests
# from invokes import invoke_http

app = Flask(__name__)
CORS(app)

exchangename = "test_email" 
exchangetype="topic" 
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
except AMQPConnectionError as e:
    print("Failed to establish connection to RabbitMQ:", str(e))
    sys.exit(1)


adoption_url = 'http://localhost:5110/submit_application'



@app.route('/create_application', methods=['POST'])
def submit_application():
    if request.is_json:
        try:
            formData = request.get_json()
            createReq(formData)
            return jsonify({
                "message":"Got it!"
            })
            # response = requests.post(adoption_url, json=request.get_json)
            # print(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "manageRequest microservice internal error: " + ex_str
            }), 500
    
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# function to publish confirmation email to notifications service
def send_notifications(formData):
    email = formData['email']
    name = formData['name']
    pet = formData['pet']
    subject = 'Confirmation of adoption request'
    # Need to change to name of user, might need to retrieve from db
    message = f"Hi {name}. This email is to confirm your adoption request for {pet}. Please track your application regularly on the website"
    body = f"{subject}, {email}, {message}"
    try:
        channel.basic_publish(exchange=exchangename, routing_key=email+'.confirm', 
                            body=body, properties=pika.BasicProperties(delivery_mode=2))
        return {'status':201, 'message': 'Confirmation email sent successfully'}
    except AMQPConnectionError as e:
        return "Failed to publish accept message due to connection error", str(e)               
    
def createReq(formData):
    # POST request to Adoption service
    print('----Sending formData to adoption service-----')
    adoption_result = requests.post(url=adoption_url, json=formData)
    print(adoption_result)
    
    # If adoption_result is (200,300), send confirmation email
    if adoption_result.status_code in range(200, 300):
            print('----Sending confirmation email to notification service -------')
            notification_result = send_notifications(formData)
            print(notification_result)
                    
    if notification_result['status'] == 201:
            # Update the pet's application
            pet_result = petApplicant(formData["petid"])
            print(pet_result)
            if pet_result:
                return jsonify({
                    "code":201,
                    "message": 'Application processed successfully'
                }), 201
    
    return jsonify({
        "code": 500,
        "message": 'Failed to send confirmation email after retries'
    }), 500
        
def petApplicant(petid):
    pet_url = f'http://localhost:8082/add/{petid}'
    result = requests.put(url=pet_url)
    print(result.status_code)
    print(result.text) 
    return result

    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)