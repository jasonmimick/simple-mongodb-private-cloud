#!/bin/bash

SERVICE_DNS=${1}
echo "Simple MongoDB Kubernetes SRV Connection Tester"
echo "Running 'host -t srv ${SERVICE_DNS}' in container image='tutum/dnsutils'"
kubectl run dnstest --restart=Never --image=tutum/dnsutils -- host -t srv pks-replica-set-svc
echo "Waiting 5 seconds for dnstest pod to deploy"
sleep 5
kubectl logs dnstest
kubectl delete pod dnstest 

echo "Running container image='jmimick/simple-mongodb-connection-tester'"

CONNECTION_STRING="mongodb://${SERVICE_DNS}/?ssl=false"
echo "Using connection string '${CONNECTION_STRING}'"
kubectl run conntester --restart=Never --image=jmimick/simple-mongodb-connection-tester ${CONNECTION_STRING}

echo "Waiting 10 seconds for conntest pod to deploy"
sleep 10
kubectl logs conntester
kubectl delete pod conntester
