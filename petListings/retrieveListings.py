from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)
CORS(app)

# CHANGE TO PUT IN .ENV FILE
databaseURL = "https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app/"
service_account_path = "../petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)