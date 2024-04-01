# Pet Adopt
A web application for pet adoption using microservices architecture.

# Notes (please read this thank you!):
1. You will need to use the **SAME EMAIL** that you used to **REGISTER** on Pet Adopt when __applying to adopt__ and __booking an appointment on Calendly. (booking page)__

2. Our Kong worked on our local machine, but **will not work for yours** as we could not figure how to load kong.yml (contains the Kong configurations) in compose.yaml. Please comment out all the relevant Kong parts in compose.yaml  **BEFORE docker compose up** to ensure that all the services and functionalities will work! This means our solution will be tested without our BTL.

# How to set up
1. All the services and yaml files are under 'app' folder
2. Set current directory to '/app' and enter 'docker compose up' in terminal to start all the services.
3. Enter 'npm run serve' to access the UI.

# Accounts to use
For admin:

  -Email: admin@gmail.com
  
  -Password: 12345!
  
You must register as a new user to test out the user-facing features and use a workable email to get the notifications.

