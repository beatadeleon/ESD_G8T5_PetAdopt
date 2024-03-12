import firebase_admin
from flask import Flask, request, jsonify 
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate(')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app'
})


# Define the route to handle the application submission
@app.route('/submit_application', methods=['POST'])
def submit_application():
    data = request.json
    adoption_request_ref = db.reference('adoptionRequests')
    new_request_ref = adoption_request_ref.push()
    new_request_ref.set({
        'requestId': new_request_ref.key,
        'userId': data['userId'],
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'message': data['message'],
        'pet': data['pet']
    })
    return jsonify({'message': 'Application submitted successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5110, debug=True)