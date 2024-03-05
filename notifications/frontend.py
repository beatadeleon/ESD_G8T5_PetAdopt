import streamlit as st
import json
import requests

# Function to make the API call
def make_api_call(email, message, action):
    url = f'http://localhost:5100/{action}'  # Replace with your API endpoint
    payload = {'email': email, 'message': message, 'action': action}
    response = requests.post(url, json=payload)
    return response

# Create a Streamlit form
with st.form("my_form"):
    # Add a text input for email address
    email = st.text_input("Email Address")


    # Add buttons for Accept and Reject
    accept = st.form_submit_button("Accept")
    reject = st.form_submit_button("Reject")
    confirm = st.form_submit_button('Confirm')
    shortlist = st.form_submit_button('Shortlist')

    # Process form submission
    if accept:
        message = f"Hi {email}. We are pleased to inform you that you have been accepted to be Boo's adopter!"
        response = make_api_call(email, message, 'accept')
        st.write(f"Accepted email: {email}, Message: {message}")
        st.write(f"API Response: {response.text}")
    elif reject:
        message = f"Hi {email}. We are regret to inform you that your application was unsuccessful. You may apply for other pets that are open for adoption."
        response = make_api_call(email, message, 'reject')
        st.write(f"Rejected email: {email}, Message: {message}")
        st.write(f"API Response: {response.text}")
    elif confirm:
        message = f"Hi {email}. This is to confirm that your application has been received!"
        response = make_api_call(email, message, 'confirm')
        st.write(f"Rejected email: {email}, Message: {message}")
        st.write(f"API Response: {response.text}")
    elif shortlist:
        message = f"Hi {email}. We are pleased to take you through the next steps. Please book appt to assess your suitability"
        response = make_api_call(email, message, 'shortlist')
        st.write(f"Rejected email: {email}, Message: {message}")
        st.write(f"API Response: {response.text}")
    
