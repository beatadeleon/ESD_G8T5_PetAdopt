from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CALDENDLY_API_KEY = 'W755XVSPKPG4AFNTNBYIZAHOQO2SNBOE'
CALENDLY_API_BASE_URL = 'https://api.calendly.com'
# Client_ID = R123_M2QGWdULfOtg52H7Xlf9Xw3QgLhVwZblbROIIc

@app.route("/cancel_event/<string:event_uuid>", methods=['POST'])
def cancel_event(event_uuid):
    url = f'{CALENDLY_API_BASE_URL}/scheduled_events/{event_uuid}/cancellation'
    reason = request.json.get('reason', '')  # Get the cancellation reason from the request JSON

    # Make a POST request to cancel the event
    response = requests.post(url, json={'reason': reason}, **get_request_configuration())

    if response.status_code == 200:
        return jsonify({"message": "Event canceled successfully"})
    else:
        return jsonify({"error": f"Error canceling event: {response.text}"}), response.status_code

 
    
if __name__ == '__main__':
		app.run(host='127.0.0.1', port=5100, debug=True)