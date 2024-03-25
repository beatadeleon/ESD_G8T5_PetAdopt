from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

adoption_URL = "http://localhost:5110/adoptionRequests/{}"
accept_URL = "http://localhost:5200/accept"
shortlisted_URL = "http://localhost:5200/shortlist"
rejected_URL = "http://localhost:5200/reject"
applications_by_pet_URL= "http://localhost:5110/adoptionRequests/petId/{}"


@app.route("/accept_request", methods=['POST'])
def accept_request():
    if request.is_json:
        try:
            # Request is from adminDashboard. Data is in the form of {"application": ..., "status": ...}
            request_data = request.get_json()
            print("\nReceived a request in JSON:", request_data)
            
            # Get the application data
            application_data = request_data["application"]
            print("\n Application data in JSON:", application_data)
            
            # Get the new status data
            new_status_data = request_data["status"]
            print("\n New status data in JSON:", new_status_data)

            # Update adoption status
            adoption_response = invoke_http(adoption_URL.format(application_data.get('requestId')), method='PUT', json={"status": new_status_data})
            print('Adoption response:', adoption_response)

            # Determine the notification URL based on the adoption status
            status = request_data.get('status')
            if status == 'pending':
                notification_URL = shortlisted_URL
            
            elif status == 'confirmed':
                notification_URL = accept_URL
                #If confirmed, get all the applicants who applied for the same pet from adoptionForm.py, and reject them
                print("This is the pet that's going to be adopted: ", application_data["petid"])
                print("This is the successful requestId: ", application_data["requestId"])
                reject_response = rejectApplicants(application_data["petid"], application_data["requestId"])
                print(reject_response)
            
            
            else:
                return jsonify({
                    "code": 400,
                    "message": f"Invalid status: {status}"
                }), 400

            # Send notification
            notification_response = invoke_http(notification_URL, method='POST', json=application_data)
            print('Notification response:', notification_response)

            return jsonify({
                "adoption_response": adoption_response,
                "notification_response": notification_response
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

# Get all the pet listings by petId, then update status to rejected for all applicants not the accepted
def rejectApplicants(petid, accepted_requestId):
    pet_applicants = invoke_http(applications_by_pet_URL.format(petid))
    reject_notifications_list =[]
    for application in pet_applicants["data"]:
        if application["requestId"] != accepted_requestId:
            # Change status 'pending' -> 'rejected'
            reject_adoption_response = invoke_http(adoption_URL.format(application.get('requestId')), method='PUT', json={"status": "rejected"})
            print("Rejected response:", reject_adoption_response)
            reject_notifications_list.append(application)
    # Batch process all rejected emails to notifications
    notification_response = invoke_http(rejected_URL, method='POST', json=reject_notifications_list)
    print('Notification response:', notification_response)

            
   

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for accepting adoption requests...")
    app.run(host="0.0.0.0", port=5400, debug=True)