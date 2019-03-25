#!/bin/bash
KUBEHOST=${KUBEHOST:-localhost}
broker_url="http://${KUBEHOST}:5000/v2/"
si_url="${broker_url}service_instances/"
# install and delete the operator

url="${si_url}my-mongodb?accepts_incomplete=false&service_id=mongodb-open-service-broker&plan_id=standard-mongodb-replset"

curl -vvv --user "admin:secret123" \
--header "Content-Type: application/json" \
--header "X-Broker-Api-Version: 2.14" \
-X PUT "${url}" \
-d @docker/mongodb-open-service-broker/samples/sample-standard-mongodb-replset.json


