kubectl-mongodb
===


Kubectl plugin for MongoDB stuff.

Install:
Clone and run `make`

Examples:

```
$kubectl mongodb operator config --user jason.mimick --publicApiKey=foo123 --project foobar
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloud-mgr-foobar-project
data:
  projectName: foobar
  baseUrl: https://cloud.mongodb.com
---
apiVersion: v1
kind: Secret
metadata:
  name: cloud-mgr-foobar-authn
type: Opaque
stringData:
  user: jason.mimick
  publicApiKey: foo123
```

or 
```
$kubectl mongodb operator config --user jason.mimick --publicApiKey=foo123 --project foobar | kubectl create -f -
configmap/cloud-mgr-foobar-project created
secret/cloud-mgr-foobar-authn created
```

```
$eval $(kubectl mongodb shell --service my-replica-set-svc)
MongoDB shell version v4.0.0
connecting to: mongodb://my-replica-set-0,my-replica-set-1,my-replica-set-2/test?ssl=false&replicaSet=my-replica-set
2018-12-03T13:50:37.135+0000 I NETWORK  [js] Starting new replica set monitor for my-replica-set/my-replica-set-0:27017,my-replica-set-1:27017,my-replica-set-2:27017
2018-12-03T13:50:37.137+0000 I NETWORK  [ReplicaSetMonitor-TaskExecutor] Successfully connected to my-replica-set-0:27017 (1 connections now open to my-replica-set-0:27017 with a 5 second timeout)
2018-12-03T13:50:37.139+0000 I NETWORK  [ReplicaSetMonitor-TaskExecutor] Successfully connected to my-replica-set-2.my-replica-set-svc.mongodb.svc.cluster.local:27017 (1 connections now open to my-replica-set-2.my-replica-set-svc.mongodb.svc.cluster.local:27017 with a 5 second timeout)
2018-12-03T13:50:37.139+0000 I NETWORK  [ReplicaSetMonitor-TaskExecutor] changing hosts to my-replica-set/my-replica-set-0.my-replica-set-svc.mongodb.svc.cluster.local:27017,my-replica-set-1.my-replica-set-svc.mongodb.svc.cluster.local:27017,my-replica-set-2.my-replica-set-svc.mongodb.svc.cluster.local:27017 from my-replica-set/my-replica-set-0:27017,my-replica-set-1:27017,my-replica-set-2:27017
2018-12-03T13:50:37.140+0000 I NETWORK  [ReplicaSetMonitor-TaskExecutor] Successfully connected to my-replica-set-0.my-replica-set-svc.mongodb.svc.cluster.local:27017 (1 connections now open to my-replica-set-0.my-replica-set-svc.mongodb.svc.cluster.local:27017 with a 5 second timeout)
2018-12-03T13:50:37.141+0000 I NETWORK  [ReplicaSetMonitor-TaskExecutor] Successfully connected to my-replica-set-1.my-replica-set-svc.mongodb.svc.cluster.local:27017 (1 connections now open to my-replica-set-1.my-replica-set-svc.mongodb.svc.cluster.local:27017 with a 5 second timeout)
MongoDB server version: 4.0.0
Server has startup warnings:
2018-11-30T18:20:27.045+0000 I CONTROL  [initandlisten]
2018-11-30T18:20:27.045+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2018-11-30T18:20:27.045+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2018-11-30T18:20:27.045+0000 I CONTROL  [initandlisten]
---
Enable MongoDB's free cloud-based monitoring service to collect and display
metrics about your deployment (disk utilization, CPU, operation statistics,
etc).

The monitoring data will be available on a MongoDB website with a unique
URL created for you. Anyone you share the URL with will also be able to
view this page. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command:
db.enableFreeMonitoring()
---

my-replica-set:PRIMARY>
```

