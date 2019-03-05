#!/bin/bash
SLEEP=10
KUBEHOST=${KUBEHOST:-localhost}
KUBECTL_DELETE_FLAGS="--grace-period=0 --force"

kubectl delete ns foobar ${KUBECTL_DELETE_FLAGS} 
kubectl delete crd mongodbreplicasets.mongodb.com ${KUBECTL_DELETE_FLAGS}
kubectl delete crd mongodbshardedclusters.mongodb.com ${KUBECTL_DELETE_FLAGS}
kubectl delete crd mongodbstandalones.mongodb.com ${KUBECTL_DELETE_FLAGS}
kubectl delete -f examples/mongodb-open-service-broker.yaml ${KUBECTL_DELETE_FLAGS}
sleep ${SLEEP}
kubectl create -f examples/mongodb-open-service-broker.yaml
sleep ${SLEEP}
kubectl create ns foobar
sleep ${SLEEP}
kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker

#BROKER_IP=""
#while [ -z "${BROKER_IP} ]; do
#  BROKER_IP=$(kubectl get service/mongodb-open-service-broker -n osbmdb-demo -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
#  sleep ${SLEEP}
#  echo "Found BROKER_IP=${BROKER_IP}"
#done

nohup kubectl port-forward deployment/mongodb-open-service-broker 5000:5000 -n osbmdb-demo &
port_forward_pid=$!
echo ">>>>>>> port_forward_pid=${port_forward_pid}"
sleep ${SLEEP}

# install and delete the operator
curl -vvv --user "admin:secret123" --header "Content-Type: application/json" --header "X-Broker-Api-Version: 2.14" -X POST "http://${KUBEHOST}:5000/v2/service_instances/myMongoKubeOperator?accepts_incomplete=false&service_id=mongodb-open-service-broker&plan_id=hello-mongodb-kubernetes-operator" -d @docker/mongodb-open-service-broker/samples/sample-kubernetes-operator.json


sleep ${SLEEP}
#kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker
#kubectl delete -f examples/mongodb-open-service-broker.yaml

sleep ${SLEEP}
curl -vvv --user "admin:secret123" --header "Content-Type: application/json" --header "X-Broker-Api-Version: 2.14" -X DELETE "http://${KUBEHOST}:5000/v2/service_instances/myMongoOpsMgr?accepts_incomplete=false&service_id=mongodb-open-service-broker&plan_id=hello-mongodb-kubernetes-operator"



#ops Manager
sleep ${SLEEP}

curl -vvv --user "admin:secret123" --header "Content-Type: application/json"  --header "X-Broker-Api-Version: 2.14" -X POST "http://${KUBEHOST}:5000/v2/service_instances/myMongoOpsMgr?accepts_incomplete=false" -d @docker/mongodb-open-service-broker/samples/sample-ops-manager.json
 

sleep ${SLEEP}
kubectl logs -n osbmdb-demo deployment/mongodb-open-service-broker

kill -9 ${port_forward_pid}
