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

@app.route("/petListings")
def get_all_listings():
    listings_ref = root_ref.child('petListings')
    listings = listings_ref.get()
    
    if listings:
        # Convert listings to a list if it's not alr one
        listings_data = [listing for listing in listings.values()]
        return jsonify({
            "code": 200, 
            "data": listings_data
        })
    else:
        return jsonify({
            "code": 404, 
            "message": "There are no listings."
        }), 404

# id is listing1,listing2 etc.
@app.route("/petListings/<string:id>")
def find_listing_by_id(id):
    listing_ref = root_ref.child(f'petListings/{id}')
    listing = listing_ref.get()
    
    if listing:
        return jsonify({
            "code": 200, 
            "data": listing
        })
    else:
        return jsonify({
            "code": 404, 
            "message": "Listing not found."
        }), 404

# add applicant
@app.route("/add/<string:id>", methods=['PUT'])
def add_applicant(id):
    listings_ref = root_ref.child('petListings')
    document_ref = listings_ref.child(id)
    document = document_ref.get()
    if document is None:
        return jsonify({'code': 404, 'message': f'ID {id} not found'}), 404
    try:
        new_applicants = document.get('applicants', 0) + 1
        document_ref.update({'applicants': new_applicants})
        return jsonify({
            'message': f'ADD success. New applicant number for {id}: {new_applicants}'
        }), 200
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Internal server error: {str(e)}'}), 500
            


   
# remove applicant
@app.route("/remove/<string:id>", methods=['PUT'])
def remove_applicant(id):
    listings_ref = root_ref.child('petListings')
    document_ref = listings_ref.child(id)
    document = document_ref.get()
    if document is None:
        return jsonify({'code': 404, 'message': f'ID {id} not found'}), 404
    try:
        if document.get('applicants') == 0:
            return jsonify({'code': 400,
                            'message': f'CANNOT remove. Applicant number for {id} is already 0. '})
        else:
            new_applicants = document.get('applicants', 0) - 1
            document_ref.update({'applicants': new_applicants})
            return jsonify({
                'message': f'REMOVE success. New applicant number for {id}: {new_applicants}'
            }), 200
    except Exception as e:
        return jsonify({'code': 500, 'message': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
