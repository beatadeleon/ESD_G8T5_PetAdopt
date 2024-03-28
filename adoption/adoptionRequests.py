from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Adoption microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create, retrieve, update, of adoption aplication'
}
swagger = Swagger(app)

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
    """
    Submit an adoption application
    ---
    tags:
      - Applications
    requestBody:
        description: Application data
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        userId:
                            type: string
                            description: The ID of the user submitting the application
                        name:
                            type: string
                            description: The name of the applicant
                        email:
                            type: string
                            format: email
                            description: The email of the applicant
                        phone:
                            type: string
                            description: The phone number of the applicant
                        message:
                            type: string
                            description: Additional message from the applicant
                        pet:
                            type: string
                            description: The pet being applied for
                        petid:
                            type: string
                            description: The ID of the pet being applied for
    responses:
      201:
        description: Application submitted successfully
      400:
        description: Invalid request data
    """
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
    """
    Get all open adoption applications
    ---
    tags:
      - Applications
    responses:
      200:
        description: A list of all open adoption applications
      404:
        description: No open applications found
    """
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
    """
    Get all pending adoption applications
    ---
    tags:
      - Applications
    responses:
      200:
        description: A list of all pending adoption applications
      404:
        description: No pending applications found
    """
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
    
@app.route("/adoptionRequests/accept")
def get_all_accepted_applications():
    """
    Get all accept adoption applications
    ---
    tags:
      - Applications
    responses:
      200:
        description: A list of all accepted adoption applications
      404:
        description: No accepted applications found
    """
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        accept_applications = [application for application in applications.values() if application.get('status') == 'accept']
        if accept_applications:
            return jsonify({
                "code": 200,
                "data": accept_applications
            })
        else:
            return jsonify({
                "code": 404,
                "message": "There are no accepted applications."
            }), 404
    else:
        return jsonify({
            "code": 404,
            "message": "There are no applications."
        }), 404
    
@app.route("/adoptionRequests/reject")
def get_all_rejected_applications():
    """
    Get all rejected adoption applications
    ---
    tags:
      - Applications
    responses:
      200:
        description: A list of all rejected adoption applications
      404:
        description: No rejected applications found
    """
    application_ref = root_ref.child('adoptionRequests')
    applications = application_ref.get()

    if applications:
        reject_applications = [application for application in applications.values() if application.get('status') == 'reject']
        if reject_applications:
            return jsonify({
                "code": 200,
                "data": reject_applications
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
    """
    Update the status of an adoption application by ID
    ---
    tags:
      - Applications
    parameters:
      - name: id
        in: path
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                description: The new status for the application
    responses:
      200:
        description: Application status updated successfully
      400:
        description: Invalid request data
      404:
        description: Application not found
    """
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
    """
    Get all adoption applications by user ID
    ---
    tags:
      - Applications
    parameters:
      - name: userId
        in: path
        type: string
        required: true
        description: The ID of the user
    responses:
      200:
        description: A list of all adoption applications for the specified user
      404:
        description: No applications found for the specified user
    """
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
    """
    Get all adoption applications by pet ID
    ---
    tags:
      - Applications
    parameters:
      - name: petid
        in: path
        type: string
        required: true
        description: The ID of the pet
    responses:
      200:
        description: A list of all adoption applications for the specified pet
      404:
        description: No applications found for the specified pet
    """
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
    """
    Get an adoption application by ID
    ---
    tags:
      - Applications
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the adoption application
    responses:
      200:
        description: Details of the adoption application
      404:
        description: Application not found
    """
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