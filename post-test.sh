#!/bin/bash
SLEEP=7
kubectl delete ns foobar
kubectl delete -f examples/mongodb-open-service-broker.yaml
sleep ${SLEEP}
kubectl create -f examples/mongodb-open-service-broker.yaml
sleep ${SLEEP}
kubectl create ns foobar
sleep ${SLEEP}
kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker

nohup kubectl port-forward deployment/mongodb-open-service-broker 5000:5000 -n osbmdb-demo &
port_forward_pid=$!
echo ">>>>>>> port_forward_pid=${port_forward_pid}"
sleep ${SLEEP}

curl -vvv --user "admin:secret123" --header "Content-Type: application/json"  --header "X-Broker-Api-Version: 2.14" -X PUT "http://localhost:5000/v2/service_instances/myMongoOpsMgr?accepts_incomplete=false" -d @docker/mongodb-open-service-broker/samples/sample-provision-1.json

sleep ${SLEEP}
kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker
#kubectl delete -f examples/mongodb-open-service-broker.yaml
kill -9 ${port_forward_pid}
