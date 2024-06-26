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
    'title': 'Accept Request complex microservice',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Invokes adoption and notification microservice'
}
swagger = Swagger(app)

# Get env variables
adoption_URL = os.environ.get("adoption_URL")
requests_by_petid_URL = os.environ.get("requests_by_petid_URL")
remove_pet_URL = os.environ.get("remove_pet_URL")

@app.route("/accept_request", methods=['POST'])
def accept_request():
    """
    Process adoption requests and send notifications.
    ---
    requestBody:
      description: Adoption request data
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              application:
                type: object
                description: The adoption application data
              status:
                type: string
                description: The new status for the adoption application
    responses:
      200:
        description: Adoption request processed successfully
      400:
        description: Invalid JSON input
      500:
        description: Internal server error
    """
    if request.is_json:
        try:
            # Request is from adminDashboard. Data is in the form of {"application": ..., "status": ...}
            request_data = request.get_json()
            print("\nReceived a request in JSON:", request_data)
            
            # Get the application data
            application_data = request_data["application"]
            print("\n Application data in JSON:", application_data)
            
            # Get the new status data
            new_status = request_data["status"]
            print("\n New status data in JSON:", new_status)

            # Update adoption status
            adoption_response =invoke_http(adoption_URL.format(application_data.get('requestId')), method='PUT', json={"status": new_status})
            print('Adoption response:', adoption_response)
            
            # Set remove_pet_response as "" so that there'll be no error for pending and else statuses
            remove_pet_response = ""
            
            # Determine the notification URL based on the adoption status
            if new_status == 'pending':
                notification_response = send_notifications(application_data, new_status)
                print('Notification response:', notification_response)
            
            # If confirmed -> send accept email to confirmed applicant, reject emails to other applicants
            elif new_status == 'accept':
                notification_response = send_notifications(application_data, new_status)
                reject_response = notify_rejected_applicants(application_data["requestId"], application_data["petid"], "reject")
                remove_pet_response = invoke_http(remove_pet_URL.format(application_data.get('petid')), method='DELETE')
                print("Batch reject response: ", reject_response)
            else:
                return jsonify({
                    "code": 400,
                    "message": f"Invalid status: {new_status}"
                }), 400            

            return jsonify({
                "adoption_response": adoption_response,
                "notification_response": notification_response,
                "remove_pet_response": remove_pet_response
            }), 200

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

# Batch rejection
def notify_rejected_applicants(accepted_requestId, petid, status):
    """
    Batch rejection of adoption requests.
    ---
    parameters:
      - name: accepted_requestId
        in: body
        description: The ID of the accepted adoption request
        required: true
      - name: petid
        in: body
        description: The ID of the pet
        required: true
      - name: status
        in: path
        description: The rejection status
        required: true
    responses:
      201:
        description: Batch rejection successful
      500:
        description: Error in batch rejection
    """
    pet_applications = invoke_http(requests_by_petid_URL.format(petid))
    reject = True
    for application in pet_applications["data"]:
        if application['requestId'] != accepted_requestId:
            try:
                reject_status = invoke_http(adoption_URL.format(application['requestId']), method='PUT', json={"status": status})
                print("Rejection status update: ", reject_status)
            except:
                reject = False
                return jsonify({"status": 500, "message": "Error updating reject status"})
            try:
                reject_response = send_notifications(application, status)
                print("Rejection response: ", reject_response)
            except:
                reject = False
                return jsonify({"status": 500, "message": "Error publishing rejection email"})
    if reject == True:
        return jsonify({"status": 201, "message": "Batch rejection successful"}), 201
        

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for accepting adoption requests...")
    app.run(host="0.0.0.0", port=5400, debug=True)