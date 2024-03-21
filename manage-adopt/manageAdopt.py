from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
# from invokes import invoke_http

app = Flask(__name__)
CORS(app)

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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Accept request microservice internal error: " + ex_str
            }), 500
    
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
            
    
def createReq(formData):
    # POST request to Adoption service
    print('----Sending formData to adoption service-----')
    adoption_result = requests.post(url=adoption_url, json=formData)
    
    # If adoption_result is 200, send confirmation email
    if adoption_result.status_code in range(200, 300):
        print('----Sending confirmation email to notification service -------')
        notification_result = requests.post(url=notification_url, json=formData)
    
    if notification_result in range(200,300) and adoption_result.status_code in range(200, 300):
        # Update the pet's application
        pet_result = petApplicant(formData.pet)
        return jsonify({
            "message": "Application processed successfully!"
        })
        
def petApplicant(pet):
    pass

    
    
    
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)