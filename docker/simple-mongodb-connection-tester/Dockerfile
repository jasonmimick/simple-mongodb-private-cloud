FROM python:2

COPY ./ ./
RUN apt-get update
RUN apt-get install -y libsnappy-dev
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT [ "python", "simple-connection-test.py" ]
CMD []
