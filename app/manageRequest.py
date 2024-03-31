from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http
from send_notifications import send_notifications
# For API docs
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Manage Request complex microservice',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Invokes petListing, adoption and notification microservice'
}
swagger = Swagger(app)

# Get env variables
adoption_URL = "http://localhost:8000/adoption/adoptionRequests/{}"
pet_url = "http://localhost:8000/petListings/remove_applicants/{}"

# adoption_url = os.environ.get("adoption_url")
# pet_url = os.environ.get("pet_url")

@app.route('/create_application', methods=['POST'])
def submit_application():
    """
    Submit an adoption application and send notifications.
    ---
    requestBody:
      description: Adoption application data
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
      200:
        description: Application submitted successfully
      400:
        description: Invalid JSON input
      500:
        description: Internal server error
    """
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
                "message": "manageRequest microservice internal error: " + ex_str
            }), 500
    
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
                
def createReq(formData):
    """
    Process the adoption application, send notifications, and update pet's application.
    ---
    parameters:
      - name: formData
        in: body
        description: Adoption application data
        required: true
    responses:
      201:
        description: Application processed successfully
      500:
        description: Failed to send confirmation
    """
    
    # POST request to Adoption service
    print('----Sending formData to adoption service-----')
    adoption_result = invoke_http(url=adoption_url, method='POST', json=formData)
    print(adoption_result)
    
    # If adoption_result is (200,300), send confirmation email
    if adoption_result['code'] in range(200, 300):
            print('----Sending confirmation email to notification service -------')
            notification_result = send_notifications(formData, 'open')
            print(notification_result)
                    
    if notification_result['code'] == 201:
            # Update the pet's application
            pet_result = petApplicant(formData["petid"])
            print(pet_result)
            if pet_result:
                return jsonify({
                    "code":201,
                    "message": 'Application processed successfully',
                    "data": formData
                }), 201
    
    return jsonify({
        "code": 500,
        "message": 'Failed to send confirmation'
    }), 500
        
def petApplicant(petid):
    """
    Update pet's application.
    ---
    parameters:
      - name: petid
        in: body
        description: The ID of the pet
        required: true
    responses:
      200:
        description: Pet's application updated successfully
      500:
        description: Failed to update pet's application
    """
    result = invoke_http(pet_url.format(petid), method='PUT')
    return result

        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)