FROM python:3-slim
WORKDIR /usr/src/app

# Copy requirement text file from the root directory
COPY ./http.reqs.txt ./

# Install requirements
RUN python -m pip install --no-cache-dir -r ./http.reqs.txt

# Copy application files
COPY ./booking.py ./
COPY ./petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json ./

# Set the environment variables
ENV DATABASE_URL="https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app/"
ENV SERVICE_ACCOUNT_PATH="./petadopt-e0fe8-firebase-adminsdk-l81sh-f8914d3037.json"

# Set the command to run the application
CMD [ "python", "./booking.py" ]
