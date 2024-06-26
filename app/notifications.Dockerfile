FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r ./amqp.reqs.txt
COPY ./notifications.py ./send_email.py ./amqp_connection.py ./
CMD [ "python", "./notifications.py" ]