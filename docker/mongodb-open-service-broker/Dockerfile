FROM python:3.6.6-alpine3.7
EXPOSE 5000

LABEL maintainer="jason.mimick@mongodb.com"
LABEL description="An Open Service API broker implementation that supports various kinds of MongoDB Deployments."
LABEL source="https://github.com/jasonmimick/simple-mongodb-private-cloud"


COPY requirements.txt ./
RUN apk --update add build-base openssl-dev libffi-dev supervisor mongodb
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN mkdir /broker/db

#Patch python jube api
COPY broker/v1beta1_custom_resource_definition_status.py /usr/local/lib/python3.6/site-packages/kubernetes/client/models/v1beta1_custom_resource_definition_status.py 
CMD [ "supervisord", "-c", "./broker/supervisord.conf" ]
