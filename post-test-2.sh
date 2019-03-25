#!/bin/bash
SLEEP=10
KUBEHOST=${KUBEHOST:-localhost}
KUBECTL_DELETE_FLAGS="--grace-period=0 --force"
nohup kubectl port-forward deployment/mongodb-open-service-broker 5000:5000 -n osbmdb-demo &
port_forward_pid=$!
echo ">>>>>>> port_forward_pid=${port_forward_pid}"
sleep ${SLEEP}

broker_url="http://${KUBEHOST}:5000/v2/"
si_url="${broker_url}service_instances/"
# install and delete the operator

url="${si_url}myMongoKubeOperator?accepts_incomplete=false&service_id=mongodb-open-service-broker&plan_id=hello-mongodb-kubernetes-operator"

#curl -vvv --user "admin:secret123" \
#--header "Content-Type: application/json" \
#--header "X-Broker-Api-Version: 2.14" \
#-X PUT "${url}" \
#-d @docker/mongodb-open-service-broker/samples/sample-kubernetes-operator.json


sleep ${SLEEP}
#kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker
#kubectl delete -f examples/mongodb-open-service-broker.yaml

#sleep ${SLEEP}
#curl -vvv --user "admin:secret123" \
#--header "Content-Type: application/json" \
#--header "X-Broker-Api-Version: 2.14" \
#-X DELETE "${url}" 


#ops Manager
#sleep ${SLEEP}

url="${si_url}myMongoOpsMgr?accepts_incomplete=false&service_id=mongodb-open-service-broker&plan_id=hello-mongodb-ops-manager"

curl -vvv --user "admin:secret123" \
--header "Content-Type: application/json" \
--header "X-Broker-Api-Version: 2.14" \
-X PUT "${url}" \
-d @docker/mongodb-open-service-broker/samples/sample-ops-manager.json
 

sleep ${SLEEP}
kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker

kill -9 ${port_forward_pid}
