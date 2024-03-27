from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http
from send_notifications import send_notifications
app = Flask(__name__)
CORS(app)

adoption_URL = "http://localhost:5110/adoptionRequests/{}"
# cancel_url ='http://localhost:5500/cancel'
# booking_url

@app.route("/cancel_request", methods=['POST'])
def cancel_request():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            request_data = request.get_json().get("request")
            print("\nReceived a request in JSON:", request_data)

            # Update adoption status
            adoption_response = invoke_http(adoption_URL.format(request_data.get('requestId')), method='PUT', json={"status": "cancel"})
            print('Adoption response:', adoption_response)

            # Send notification
            notification_response = send_notifications(request_data, "cancel")
            print('Notification response', notification_response)

            return jsonify({
                "adoption_response": adoption_response,
                "notification_response": notification_response
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
