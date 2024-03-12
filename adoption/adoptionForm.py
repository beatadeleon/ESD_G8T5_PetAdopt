from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os


app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

databaseURL = os.getenv('DATABASE_URL')
service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')

cred_obj = firebase_admin.credentials.Certificate(service_account_path)
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})

# Reference to db
root_ref = db.reference()


# Push application form to database
@app.route('/submit_application', methods=['POST'])
def submit_application():
    data = request.json

    if data is None:
        return jsonify({'error': 'Invalid request data.'}), 400

    try:
        userId = data['userId']
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        pet = data['pet']
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e.args[0]}'}), 400
    except TypeError:
        return jsonify({'error': 'Invalid request data format.'}), 400

    adoption_request_ref = root_ref.child('adoptionRequests')
    new_request_ref = adoption_request_ref.push()
    new_request_ref.set({
        'requestId': new_request_ref.key,
        'userId': userId,
        'name': name,
        'email': email,
        'phone': phone,
        'message': message,
        'pet': pet
    })

    return jsonify({'message': 'Application submitted successfully!'})


@app.route("/adoptionRequests/open")
def get_all_open_applications():
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        open_applications = [application for application in applications.values() if application.get('status') == 'open']
        if open_applications:
            return jsonify({
                "code": 200,
                "data": open_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": "There are no open applications."
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404


@app.route("/adoptionRequests/<string:id>")
def find_application_by_id(id):
    application_ref = root_ref.child(f'adoptionRequests/{id}')
    application = application_ref.get()
    
    if application:
        return jsonify({
            "code": 200, 
            "data": application
        })
    else:
        return jsonify({
            "code": 404, 
            "message": "Application not found."
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5110, debug=True)