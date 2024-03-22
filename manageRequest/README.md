### How to setup manageRequest complex 

1. Run the notifications service (notifications folder) in the following
    1. Run RabbitMQ container on Docker first
    2. amqp_connection.py > ampq_setup.py > notifications.py
    3. Run email_service.py if you want to get the email immediately

2. Run adoption/adoptionForm.py
3. Run petListings/retrieveListings.py
4. Run manageRequest/manageRequest.py