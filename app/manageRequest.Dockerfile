FROM python:3-slim
WORKDIR /usr/src/app

# Copy requirement text file from the root directory
COPY ./http.reqs.txt ./amqp.reqs.txt ./

# Install requirements
RUN python -m pip install --no-cache-dir -r ./http.reqs.txt
RUN python -m pip install --no-cache-dir -r ./amqp.reqs.txt

# Copy application files
COPY ./manageRequest.py ./send_notifications.py ./invokes.py ./amqp_connection.py ./
COPY ./petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json ./

# Set the environment variables
ENV DATABASE_URL="https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app/"
ENV SERVICE_ACCOUNT_PATH="./petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json"

# Set the command to run the application
CMD [ "python", "./manageRequest.py"]
