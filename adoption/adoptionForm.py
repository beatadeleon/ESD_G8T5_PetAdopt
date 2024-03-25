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
        petId = data['petid']

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
        'pet': pet,
        'petid': petId,
        'status': 'open'
    })

    return jsonify({'message': 'Application submitted successfully!'}), 201


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
    
@app.route("/adoptionRequests/pending")
def get_all_pending_applications():
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        pending_applications = [application for application in applications.values() if application.get('status') == 'pending']
        if pending_applications:
            return jsonify({
                "code": 200,
                "data": pending_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": "There are no pending applications."
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404
    
@app.route("/adoptionRequests/confirmed")
def get_all_confirmed_applications():
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        confirmed_applications = [application for application in applications.values() if application.get('status') == 'confirmed']
        if confirmed_applications:
            return jsonify({
                "code": 200,
                "data": confirmed_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": "There are no confirmed applications."
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404
    
@app.route("/adoptionRequests/rejected")
def get_all_rejected_applications():
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        rejected_applications = [application for application in applications.values() if application.get('status') == 'rejected']
        if rejected_applications:
            return jsonify({
                "code": 200,
                "data": rejected_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": "There are no rejected applications."
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404

# Update application status using requestId
@app.route("/adoptionRequests/<string:id>", methods=['PUT'])
def update_application_status(id):
    data = request.json

    if 'status' not in data:
        return jsonify({"status": "open"}), 400

    status = data['status']
    application_ref = root_ref.child(f'adoptionRequests/{id}')

    if application_ref.get():
        application_ref.update({'status': status})
        return jsonify({'message': f'Status updated to {status}.'})
    else:
        return jsonify({'error': 'Application not found.'}), 404

# Get all requests by userId
@app.route("/adoptionRequests/userId/<string:userId>")
def get_listing_by_userId(userId):
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        user_applications = [application for application in applications.values() if application.get('userId') == userId]
        if user_applications:
            return jsonify({
                "code": 200,
                "data": user_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": f"No applications found for userId: {userId}"
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404
        
# Get all requests by petid
@app.route("/adoptionRequests/petid/<string:petid>")
def get_listing_by_petid(petid):
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        pet_applications = [application for application in applications.values() if application.get('petid') == petid]
        if pet_applications:
            return jsonify({
                "code": 200,
                "data": pet_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": f"No applications found for petid: {petid}"
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404

# Get request using requestId
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