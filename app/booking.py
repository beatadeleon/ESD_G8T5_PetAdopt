from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
from dotenv import load_dotenv

from flasgger import Swagger

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load environment variables
load_dotenv()

databaseURL = os.getenv('DATABASE_URL')
service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')

cred_obj = firebase_admin.credentials.Certificate(service_account_path)
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Booking microservice calendly API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Update Uuid and cancel scheduled booking'
}
swagger = Swagger(app)


CALENDLY_API_KEY = os.getenv('VUE_APP_CALENDLY_API_KEY')
CALENDLY_BASE_URL = 'https://api.calendly.com'



@app.route("/update_calendly_uuid", methods=['POST'])
def update_calendly_uuid():
    """
    Update Calendly UUID for a user
    ---
    requestBody:
        description: User's data
        required: true
        content:
            application/json:
                schema:
                    properties:
                        email: 
                            type: string
                            description: User's email
                        calendlyUuid: 
                            type: string
                            description: User's Calendly UUID
    responses:
        200:
            description: Calendly UUID updated successfully
        400:
            description: Missing email or calendlyUuid in the request
        404:
            description: User not found or No users with the provided email
        500:
            description: An error occurred during the operation
    """
    if request.is_json:
        try:
            data = request.get_json()
            userEmail = data.get('email')
            calendly_uuid = data.get('calendlyUuid')

            print("DEBUG:", type(data), data)

            if not userEmail or not calendly_uuid:
                return jsonify({
                    "code": 400,
                    "message": "Missing email or calendlyUuid in the request"
                }), 400

            users_ref = db.reference('users')
            query_result = users_ref.order_by_child('email').equal_to(userEmail).get()

            if query_result:
                for user_id, user_info in query_result.items():
                    if user_info['email'] == userEmail:
                        user_ref = db.reference(f'users/{user_id}')
                        user_ref.update({'calendlyUuid': calendly_uuid})
                        return jsonify({
                            "code": 200,
                            "message": "Calendly UUID updated successfully"
                        }), 200
                return jsonify({
                    "code": 404,
                    "message": "User not found"
                }), 404
            else:
                return jsonify({
                    "code": 404,
                    "message": "No users with the provided email"
                }), 404

        except Exception as e:
            return jsonify({
                "code": 500,
                "message": "An error occurred: " + str(e)
            }), 500
    else:
        return jsonify({
            "code": 400,
            "message": "Request must be JSON"
        }), 400

@app.route("/process_cancellation", methods=['POST'])
def process_cancellation():
    """
    Process cancellation of Calendly booking for a user
    ---
    requestBody:
        description: User's data
        required: true
        content:
            application/json:
                schema:
                    properties:
                        email: 
                            type: string
                            description: User's email
    responses:
        200:
            description: Calendly booking cancelled successfully
        400:
            description: Invalid JSON input or email is required
        500:
            description: Internal server error during the cancellation process
    """
    if request.is_json:
        try:
            request_data = request.get_json()
            print("\nReceived cancellation request data:", request_data)

            # receive email from request
            email = request_data.get('email')
            if not email:
                raise ValueError("email is required.")

            # Get all users from Firebase
            ref = db.reference('users')
            users_data = ref.get()

            # Find the user by email
            user_data = None
            for user_id, user_info in users_data.items():
                if user_info.get('email') == email:
                    user_data = user_info
                    calendly_uuid = user_data.get('calendlyUuid')

                    if calendly_uuid != "null":
                        user_ref = db.reference(f'users/{user_id}')
                        user_ref.update({'calendlyUuid': 'null'})

                        cancel_booking_response = requests.post(
                        f"{CALENDLY_BASE_URL}/scheduled_events/{calendly_uuid}/cancellation",
                        headers={"Authorization": f"Bearer {CALENDLY_API_KEY}"}
                        )

                        if cancel_booking_response.status_code == 201:
                            print("Calendly booking cancelled successfully.")
                        else:
                            raise Exception(f"Failed to cancel Calendly booking: {cancel_booking_response.text}")
                        
                        return jsonify({
                            "code": 200,
                            "message": "Calendly booking cancelled successfully"
                        }), 200
                    
                    else:
                        print("No Calendly booking found for this user.")
                        return jsonify({
                            "code": 200,
                            "message": "No Calendly booking found for this user."
                        }), 200
                    
                else:
                    print("User not found.")
                    return jsonify({
                        "code": 404,
                        "message": "User not found."
                    }), 404
                
            if not user_data:
                raise ValueError(f"User with email {email} not found.")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = f"{e} at {exc_type}: {fname}: line {exc_tb.tb_lineno}"
            print(ex_str)
            return jsonify({"code": 500, "message": f"booking.py internal error: {ex_str}"}), 500

    return jsonify({"code": 400, "message": "[booking] Invalid JSON input"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600, debug=True)