from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

adoption_URL = "http://localhost:5110/adoptionRequests/{}"
cancel_url ='http://localhost:5500/cancel'
cancel_booking_url = 'http://localhost:5600/process_cancellation'

@app.route("/cancel_request", methods=['POST'])
def cancel_request():
    # Simple check of input format and data of the request are JSON

    # ehe
    if request.is_json:
        try:
            request_data = request.get_json()
            print(request_data)
            print("\nReceived a request in JSON:", request_data)

            # Update adoption status
            adoption_response = invoke_http(adoption_URL.format(request_data.get('requestId')), method='PUT', json=request_data)
            print('Adoption response:', adoption_response)

            #Body:
            # {
            #    "requestId": "-NtFFI_b7qhOQDT4LR-c",
            #    "status": "cancelled"
            # }

            # Send notification
            notification_response = invoke_http(cancel_url, method='POST', json=request_data)
            print('Notification response:', notification_response)

            # Send cancellation request to booking service
            email = request_data.get('email') 
            cancel_booking_response = invoke_http(
                'http://localhost:5600/process_cancellation',
                method='POST',
                json={'email': email}
            )
            print('Cancel booking response:', cancel_booking_response)

            return jsonify({
                "code": 200,
                "adoption_response": adoption_response,
                "notification_response": notification_response,
                "cancel_booking_response": cancel_booking_response 
            }), 200

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
