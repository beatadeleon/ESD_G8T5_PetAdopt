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
    'title': 'Pet listings API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Retrieves pet listings, add applicant to a pet listing, remove applicant from a pet listing, remove a pet listing once adopted'
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

@app.route("/petListings")
def get_all_listings():
    """
    Retrieve all pet listings
    ---
    responses:
      200:
        description: A list of all pet listings
    """
    listings_ref = root_ref.child('petListings')
    listings = listings_ref.get()
    
    if listings:
        # Convert listings to a list if it's not alr one
        listings_data = [listing for listing in listings.values()]
        return jsonify({
            "code": 200, 
            "data": listings_data
        }), 200
    else:
        return jsonify({
            "code": 404, 
            "message": "There are no listings."
        }), 404

# id is listing1,listing2 etc.
@app.route("/petListings/<string:id>")
def find_listing_by_id(id):
    """
    Retrieve a pet listing by ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the pet listing
    responses:
      200:
        description: Details of the pet listing
      404:
        description: Listing not found
    """
    listing_ref = root_ref.child(f'petListings/{id}')
    listing = listing_ref.get()
    
    if listing:
        return jsonify({
            "code": 200, 
            "data": listing
        }), 200
    else:
        return jsonify({
            "code": 404, 
            "message": "Listing not found."
        }), 404

# add applicant
@app.route("/add_applicants/<string:id>", methods=['PUT'])
def add_applicant(id):
    """
    Add an applicant to a pet listing
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the pet listing
    responses:
      200:
        description: Success message
      404:
        description: Listing not found
    """
    listings_ref = root_ref.child('petListings')
    document_ref = listings_ref.child(id)
    document = document_ref.get()
    if document is None:
        return jsonify({'code': 404, 'message': f'ID {id} not found'}), 404
    try:
        new_applicants = document.get('applicants', 0) + 1
        document_ref.update({'applicants': new_applicants})
        return jsonify({
              'code': 200,
            'message': f'ADD success. New applicant number for {id}: {new_applicants}'
        }), 200
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Internal server error: {str(e)}'}), 500
            


   
# remove applicant
@app.route("/remove_applicants/<string:id>", methods=['PUT'])
def remove_applicant(id):
    """
    Remove an applicant from a pet listing
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the pet listing
    responses:
      200:
        description: Success message
      404:
        description: Listing not found
    """
    listings_ref = root_ref.child('petListings')
    document_ref = listings_ref.child(id)
    document = document_ref.get()
    if document is None:
        return jsonify({'code': 404, 'message': f'ID {id} not found'}), 404
    try:
        if document.get('applicants') == 0:
            return jsonify({'code': 400,
                            'message': f'CANNOT remove. Applicant number for {id} is already 0. '}), 400
        else:
            new_applicants = document.get('applicants', 0) - 1
            document_ref.update({'applicants': new_applicants})
            return jsonify({
                'code': 200,
                'message': f'REMOVE success. New applicant number for {id}: {new_applicants}'
            }), 200
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Internal server error: {str(e)}'}), 500


# remove pet once they are adopted
@app.route("/remove/<string:id>", methods=['DELETE'])
def remove_pet(id):
    """
    Remove a pet listing once pet is adopted
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the pet listing
    responses:
      200:
        description: Success message
      404:
        description: Listing not found
    """
    listings_ref = root_ref.child('petListings')
    document_ref = listings_ref.child(id)
    try:
        document_ref.delete()
        return jsonify({
            'code': 200,
            'message': f'Successfully removed pet {id}!'
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
