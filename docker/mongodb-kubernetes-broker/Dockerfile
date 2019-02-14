FROM python:3.6.6-alpine3.7
#FROM python:3.6-alpine
EXPOSE 5000

WORKDIR /mongodb-kuberenetes-broker

COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN apk add build-base
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u", "./broker/broker.py" ]
