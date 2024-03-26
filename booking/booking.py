from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests



app = Flask(__name__)
CORS(app, supports_credentials=True)

cred = credentials.Certificate('../petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

CALENDLY_API_KEY = os.getenv('VUE_APP_CALENDLY_API_KEY')
CALENDLY_BASE_URL = 'https://api.calendly.com'



@app.route("/update_calendly_uuid", methods=['POST'])
def update_calendly_uuid():
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
    if request.is_json:
        try:
            request_data = request.get_json()
            print("\nReceived cancellation request data:", request_data)

            # receive email from request
            email = request_data.get('email')
            if not email:
                raise ValueError("email is required.")

            # get user data from firebase, check if user exists
            ref = db.reference(f'users/{email}')
            user_data = ref.get()
            if not user_data:
                raise ValueError(f"User with email {email} not found.")

            # get calendlyUuid from user data (from firebase)
            calendly_uuid = user_data.get('calendlyUuid')

            if calendly_uuid and calendly_uuid != "null":
                ref.update({'calendlyUuid': "null"})

                cancel_booking_response = requests.delete(
                    f"{CALENDLY_BASE_URL}scheduled_events/{calendly_uuid}/cancellation",
                    headers={"Authorization": f"Bearer {CALENDLY_API_KEY}"}
                )

                if cancel_booking_response.status_code == 204:
                    print("Calendly booking cancelled successfully.")
                else:
                    raise Exception(f"Failed to cancel Calendly booking: {cancel_booking_response.text}")

                return jsonify({"message": "Booking cancellation processed successfully."}), 200
            else:
                return jsonify({"message": "No booking to cancel."}), 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = f"{e} at {exc_type}: {fname}: line {exc_tb.tb_lineno}"
            print(ex_str)
            return jsonify({"code": 500, "message": f"booking.py internal error: {ex_str}"}), 500

    return jsonify({"code": 400, "message": "Invalid JSON input"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600, debug=True)