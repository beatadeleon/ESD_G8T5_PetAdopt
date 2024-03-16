from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import requests

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

adoption_url = 'http://localhost:5110/submit_application'
notification_url ='http://localhost:5200/confirm'
# pets_url
# error_url

@app.route('/create_application', methods=['POST'])
def submit_application():
    if request.is_json:
        try:
            formData = request.get_json()
            createReq(formData)
            return jsonify({
                "message":"Got it!"
            })
            # response = requests.post(adoption_url, json=request.get_json)
            # print(response)
        except:
            return 'Bad'
            
    
def createReq(formData):
    # POST request to Adoption service
    print('----Sending formData to adoption service-----')
    adoption_result = requests.post(url=adoption_url, json=formData)
    
    # If adoption_result is 200, send confirmation email
    if adoption_result.status_code in range(200, 300):
        print('----Sending confirmation email to notification service -------')
        notification_result = requests.post(url=notification_url, json=formData)
    
    if notification_result in range(200,300) and adoption_result.status_code in range(200, 300):
        return jsonify({
            "message": "Application processed successfully!"
        })

    
    
    
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)