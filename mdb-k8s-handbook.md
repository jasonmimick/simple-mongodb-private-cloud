# The MongoDB Kubernetes Handbook

*A guide to the history, design, how to get started, and resources for the
MongoDB Kubernetes Operator*

Table of Contents
===
[The MongoDB Operator](#the-mongodb-operator)

[History](#history)

[Design](#design)

[Getting Started](#getting-started)

[minikube](#minikube)

[GCE](#gce)

[Production Notes](#production-notes)

[Containerizing MongoDB Ops Manager](#containerizing-mongoDB-ops-manager)

[Namespace Considerations](#namespace-considerations)

[Resources](#resources)

Index

## The MongoDB Operator

The MongoDB Kubernetes Operator is designed to work in conjuction with MongoDB
Ops Manager](http://), which is a database cluster management system with many
features. The automation functionality of Ops Manager is used by the MongoDB
Operator to create and control database runtimes. These runtimes are, of course,
within containers running inside Pods on Worker Nodes within a Kubernetes
cluster. MongoDB Ops Manager can be installed both within or outside of the
given Kubernetes cluster or a completely cloud-based version [Cloud
Manager](https://cloud.mongodb.com) can be used.

The MongoDB Operator consists of a set of custom resource definitions
([CRDs](http://foo)), two container images, and a set of YAML artifacts. A
custom resource is defined for stand alone, replica-set, and sharded cluster
type MongoDB deployments. 

The MongoDB Operator ships two Docker images one for the operator itself and one
for the database runtime. The db runtime image contains the MongoDB Automation
Agent binaries, and it is this process which is practically<sup>1</sup> the main process for
the database container.

<sup>1</sup> *Practically*, since technically the container runs a `supervisord` process
which watches the `automation-agent` process. This is done to facilitate agent
upgrades without the container getting killed.

## Getting Started

There are a number of ways to get started using the MongoDB Kubernetes Operator,
but the most important place to start is to determine how and where you're
planning to run Kubernetes. For this guide, we focus on two particularly simple
and easy ways to get Kubernetes up and running: minikube and GCE (Google
Container Engine). But, the overall steps are similar for other Kubernetes
distributions or cloud-based services.

For both getting started options, we'll use MongoDB Cloud Manager. See
Containerizing MongoDB Ops Manager for information on running Ops Manager within
your Kubernetes cluster. Apart from needing to first install MongoDB Ops Manager,
the steps are identical.

### Download & Install Prerequisites

Install minikube: https://kubernetes.io/docs/tasks/tools/install-minikube/

Clone the mdb-k8s-op Github repository:

```bash
$# cd to directory you want to clone repository
$git clone https://github.com/mongodb/mongodb-enterprise-kubernetes
```

### Configure MongoDB Cloud Manager

1. Login or create an account at https://cloud.mongodb.com

2. Create an API Key and enable API access via whitelist: 
https://docs.cloudmanager.mongodb.com/tutorial/configure-public-api-access/

Be sure to copy and paste your API Key, you will need to add this to a
Kubernetes secret later. You should see something similar to:

##### Create a project in Cloud Manager:
https://docs.cloudmanager.mongodb.com/tutorial/manage-projects/#create-a-project

Note down your project name, for demonstration purposes, we'll use
hello-mongo-kube as our project name throughout this guide.


_Choose one option!_ Minikube  - or - GCE

### minikube

minikube is a single VM-based Kubernetes distribution which you typically run
directly on your own computer. It is widely used for development and testing
purposes, and ideally suited for your first foray into learning about running
MongoDB and Kubernetes together.

#### Create minikube cluster

[Install minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) and
then simple, default, cluster will work for this demonstration:

```bash
➜  minikube version
minikube version: v0.32.0
➜  minikube start
Starting local Kubernetes v1.12.4 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Stopping extra container runtimes...
Starting cluster components...
Verifying kubelet health ...
Verifying apiserver health ...Kubectl is now configured to use the cluster.
Loading cached images from config file.


Everything looks great. Please enjoy minikube!
➜  minikube status
host: Running
kubelet: Running
apiserver: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.99.100
```
### GCE

Full details on getting setup with Google Container Engine are beyond the scope
of this note, so please use your appropriate Google-fu and figure that out. We'l
assume you've got the `glcoud` command line tool installed, you're logged in,
you've got a project with Kubernetes Engine API enabled, and you see something
similar to the following (the important thing being there be no cluster called
`hello-mongo-kube`).

```bash
➜  ~ gcloud container clusters list
➜  ~
```

First, let's spin up a cluster.

```bash
➜  ~ gcloud container clusters create hello-mongo-kube --zone us-east1-c
Creating cluster hello-mongo-kube in us-east1-c... Cluster is being deployed...⠏
Cluster is being health-checked (master is healthy)...done.
Created [https://container.googleapis.com/v1/projects/federate-foo/zones/us-east1-c/clusters/hello-mongo-kube].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-east1-c/hello-mongo-kube?project=federate-foo
kubeconfig entry generated for hello-mongo-kube.
NAME              LOCATION    MASTER_VERSION  MASTER_IP        MACHINE_TYPE   NODE_VERSION  NUM_NODES  STATUS
hello-mongo-kube  us-east1-c  1.10.9-gke.5    104.196.210.140  n1-standard-1  1.10.9-gke.5  3          RUNNING
```
Oh, that's it. Continue on to the next step.

_NOTE_ If you hit RBAC errors when trying to install the operator in a later
step you can create the appropriate `clusterrole` for your GCE user. You can do
this step now, or come back later when (or if) you hit the error.

```bash
➜  kubectl create clusterrolebinding me-cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value core/account)
```

### Setting up the MongoDB Operator


Let's check and make sure the kubectl command is working properly:

```bash
➜  kubectl get all --all-namespaces
NAMESPACE     NAME                                        READY   STATUS    RESTARTS   AGE
kube-system   pod/coredns-576cbf47c7-ckxgk                1/1     Running   0          2m31s
kube-system   pod/coredns-576cbf47c7-pvb24                1/1     Running   0          2m31s
kube-system   pod/etcd-minikube                           1/1     Running   0          106s
kube-system   pod/kube-addon-manager-minikube             1/1     Running   0          100s
kube-system   pod/kube-apiserver-minikube                 1/1     Running   0          91s
kube-system   pod/kube-controller-manager-minikube        1/1     Running   0          100s
kube-system   pod/kube-proxy-hgllb                        1/1     Running   0          2m31s
kube-system   pod/kube-scheduler-minikube                 1/1     Running   0          90s
kube-system   pod/kubernetes-dashboard-5bff5f8fb8-h8mjz   1/1     Running   0          2m30s
kube-system   pod/storage-provisioner                     1/1     Running   0          2m29s

NAMESPACE     NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
default       service/kubernetes             ClusterIP   10.96.0.1       <none>        443/TCP         2m41s
kube-system   service/kube-dns               ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP   2m36s
kube-system   service/kubernetes-dashboard   ClusterIP   10.102.210.59   <none>        80/TCP          2m29s

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
kube-system   daemonset.apps/kube-proxy   1         1         1       1            1           <none>          2m36s

NAMESPACE     NAME                                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kube-system   deployment.apps/coredns                2         2         2            2           2m36s
kube-system   deployment.apps/kubernetes-dashboard   1         1         1            1           2m30s

NAMESPACE     NAME                                              DESIRED   CURRENT   READY   AGE
kube-system   replicaset.apps/coredns-576cbf47c7                2         2         2       2m31s
kube-system   replicaset.apps/kubernetes-dashboard-5bff5f8fb8   1         1         1       2m30s
```

#### Create Kubernetes Namespace

By default, the MongoDB Kubernetes Operator will attempt to install and watch
for database resource events in a namespace called mongodb. This can be
customized in different ways, see Namespace Considerations for more information.
For this example we'll just use the default, and to do so, we need to create
this namespace. The follow code snippet shows creating the namespace, verifying
it's there, and then setting mongodb to be the default namespace for kubectl.

```bash
➜  kubectl create namespace mongodb
namespace/mongodb created
➜  kubectl get namespaces
NAME          STATUS   AGE
default       Active   9m55s
kube-public   Active   9m50s
kube-system   Active   9m55s
mongodb       Active   32s
➜  kubectl config set-context $(kubectl config current-context) --namespace mongodb
Context "minikube" modified.
➜  kubectl get all
No resources found.
```

#### Install MongoDB Kubernetes Operator

In this step we will install the CRDs and Operator itself into Kubernetes.

```bash
➜  mongodb-enterprise-kubernetes
➜  kubectl create -f crds.yaml
customresourcedefinition.apiextensions.k8s.io/mongodbstandalones.mongodb.com created
customresourcedefinition.apiextensions.k8s.io/mongodbreplicasets.mongodb.com created
customresourcedefinition.apiextensions.k8s.io/mongodbshardedclusters.mongodb.com created
➜  kubectl create -f mongodb-enterprise.yaml
role.rbac.authorization.k8s.io/mongodb-enterprise-operator created
rolebinding.rbac.authorization.k8s.io/mongodb-enterprise-operator created
serviceaccount/mongodb-enterprise-operator created
deployment.apps/mongodb-enterprise-operator created
```

We can verify things installed and the operator is running with a few other
commands:

```bash
➜  kubectl get crds | grep mongodb
mongodbreplicasets.mongodb.com       2019-01-18T13:28:14Z
mongodbshardedclusters.mongodb.com   2019-01-18T13:28:14Z
mongodbstandalones.mongodb.com       2019-01-18T13:28:10Z
➜  kubectl get all
NAME                                               READY   STATUS    RESTARTS   AGE
pod/mongodb-enterprise-operator-5c9c9b764b-2bcz4   1/1     Running   0          2m42s

NAME                                          DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mongodb-enterprise-operator   1         1         1            1           2m42s

NAME                                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/mongodb-enterprise-operator-5c9c9b764b   1         1         1       2m42s
➜  kubectl logs deployment.apps/mongodb-enterprise-operator
{"level":"info","ts":1547818116.3835168,"caller":"ops-manager-kubernetes/main.go:74","msg":"Operator environment: prod"}
{"level":"info","ts":1547818116.383644,"caller":"ops-manager-kubernetes/main.go:75","msg":"Go Version: go1.11.3"}
{"level":"info","ts":1547818116.3837543,"caller":"ops-manager-kubernetes/main.go:76","msg":"Go OS/Arch: linux/amd64"}
<... many lines omitted ...>
{"level":"info","ts":1547818116.3840683,"caller":"util/util.go:157","msg":"\tWATCH_NAMESPACE=mongodb"}
{"level":"info","ts":1547818116.4335158,"caller":"ops-manager-kubernetes/main.go:47","msg":"Registering Components."}
{"level":"info","ts":1547818116.4338334,"caller":"operator/mongodbstandalone_controller.go:46","msg":"Registered controller mongodbstandalone-controller"}
{"level":"info","ts":1547818116.433938,"caller":"operator/mongodbreplicaset_controller.go:135","msg":"Registered controller mongodbreplicaset-controller"}
{"level":"info","ts":1547818116.4339912,"caller":"operator/shardedclusterkube.go:234","msg":"Registered controller mongodbshardedcluster-controller"}
{"level":"info","ts":1547818116.434018,"caller":"ops-manager-kubernetes/main.go:59","msg":"Starting the Cmd."}
```

There's quite a bit of log data, the important thing is the "Starting the Cmd."
at the end. We should be ready for the next step.

#### Configure MongoDB Kubernetes Operator

The last step before we can start deploying MongoDB into this new cloud-native
environment is to add two configuration items into our Kubernetes cluster. These
two items, a ConfigMap and a Secret, are referenced by MongoDB database
deployment definitions and accessed at run-time by the operator. They store
connection information so that the operator can communicate securely with your
Ops Manager, or Cloud Manager in this case, instance.

##### Create Secret for Cloud Manager credentials:

We'll create a secret called cloud-manager. Replace your user and publicApiKey
below appropriately:

```bash
➜  kubectl create secret generic cloud-manager \
--from-literal="user=<YOUR USER HERE" \        --from-literal="publicApiKey=<YOUR PUBLIC API KEY>"
secret/cloud-manager created
➜  kubectl describe secret cloud-manager
Name:         cloud-manager
Namespace:    mongodb
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
publicApiKey:  36 bytes
user:          12 bytes
```

See: https://docs.opsmanager.mongodb.com/current/tutorial/install-k8s-operator/index.html#create-credentials

##### Create ConfigMap for Cloud Manager project:

Edit and save a file called hello-mongo-kube-project.yaml with the following
content:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-mongo-kube
  namespace: mongodb
data:
  projectName: hello-mongo-kube
  baseUrl: https://cloud.mongodb.com
```

Now we can push this to Kubernetes and inspect for verification:

```bash
➜  kubectl create -f hello-mongo-kube-project.yaml
configmap/hello-mongo-kube created
➜  kubectl describe configmap hello-mongo-kube
Name:         hello-mongo-kube
Namespace:    mongodb
Labels:       <none>
Annotations:  <none>

Data
====
baseUrl:
----
https://cloud.mongodb.com
projectName:
----
hello-mongo-kube
Events:  <none>
```

See: https://docs.opsmanager.mongodb.com/current/tutorial/install-k8s-operator/index.html#create-your-onprem-project-and-k8s-k8s-configmap

#### Deploy a MongoDB Replica Set

Finally, we're ready to get a database up and running. The good news is that all
the setup and configuration we just went through is only needed once! (If you
want to organize your MongoDB databases into multiple different Ops Manager
projects, then you'll need a ConfigMap for each one.)

Each database configuration is defined in a yaml file, so to create a basic
starter MongoDB replica set, create and edit a file like so,

```bash
➜  mongodb-enterprise-kubernetes git:(master) ✗ cat hello-db.yaml
```

```yaml
---
apiVersion: mongodb.com/v1
kind: MongoDbReplicaSet
metadata:
  name: hello-db
  namespace: mongodb
spec:
  members: 3
  version: 4.0.0
  project: hello-mongo-kube
  credentials: cloud-manager
  persistent: true
```

In another shell session you can follow the operator logs to watch things happen
when deploying a MongoDB replica set in the next step.

```bash
➜  kubectl logs -f deployment.apps/mongodb-enterprise-operator
{"level":"info","ts":1547822529.6096876,"caller":"ops-manager-kubernetes/main.go:74","msg":"Operator environment: prod"}
{"level":"info","ts":1547822529.6098433,"caller":"ops-manager-kubernetes/main.go:75","msg":"Go Version: go1.11.3"}
< ... omitted ... >
{"level":"info","ts":1547822529.7055557,"caller":"ops-manager-kubernetes/main.go:59","msg":"Starting the Cmd."}
```

Next, provision the database cluster through Kubernetes:

```bash
➜  kubectl create -f hello-db.yaml
mongodbreplicaset.mongodb.com/hello-db created
➜  kubectl get all
NAME                                               READY   STATUS    RESTARTS   AGE
pod/hello-db-0                                     1/1     Running   0          39s
pod/hello-db-1                                     1/1     Running   0          37s
pod/hello-db-2                                     1/1     Running   0          33s
pod/mongodb-enterprise-operator-5c9c9b764b-vlqcc   1/1     Running   0          5m51s

NAME                            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
service/hello-db-svc            ClusterIP   None            <none>        27017/TCP         40s
service/hello-db-svc-external   NodePort    10.101.80.243   <none>        27017:30654/TCP   40s

NAME                                          DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mongodb-enterprise-operator   1         1         1            1           79m

NAME                                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/mongodb-enterprise-operator-5c9c9b764b   1         1         1       79m

NAME                        DESIRED   CURRENT   AGE
statefulset.apps/hello-db   3         3         40s
```

In the operator logs, you should see something like:

```json
{"level":"info","ts":1547822837.944861,"caller":"operator/kubehelper.go:261","msg":"Service doesn't exist - creating it","ReplicaSet":"mongodb/hello-db","service":"hello-db-svc-external"}
{"level":"info","ts":1547822837.9751043,"caller":"operator/kubehelper.go:267","msg":"Created service","ReplicaSet":"mongodb/hello-db","service":"hello-db-svc-external","type":"NodePort","port":{"protocol":"TCP","port":27017,"targetPort":27017,"nodePort":30654}}
{"level":"info","ts":1547822837.9996543,"caller":"operator/kubehelper.go:194","msg":"Waiting until statefulset and its pods reach READY state...","ReplicaSet":"mongodb/hello-db","statefulset":"hello-db"}
{"level":"info","ts":1547822848.0013993,"caller":"operator/kubehelper.go:206","msg":"Created statefulset","ReplicaSet":"mongodb/hello-db","statefulset":"hello-db","time":10.176720956}
{"level":"info","ts":1547822848.0014863,"caller":"operator/mongodbreplicaset_controller.go:99","msg":"Updated statefulset for replica set","ReplicaSet":"mongodb/hello-db"}
{"level":"info","ts":1547822848.0015135,"caller":"operator/common.go:116","msg":"Waiting for agents to register with OM","ReplicaSet":"mongodb/hello-db","statefulset":"hello-db","agent hosts":["hello-db-0.hello-db-svc.mongodb.svc.cluster.local","hello-db-1.hello-db-svc.mongodb.svc.cluster.local","hello-db-2.hello-db-svc.mongodb.svc.cluster.local"]}
```

_NOTE_: When using Cloud Manager it seems the wildcard ip 0.0.0.0/0 doesn't get
applied correctly. If you see messages like this in the operator logs, then add
the IP from the error message to your Cloud Manager whitelist.

```json
{"level":"error","ts":1547819819.422789,"caller":"operator/controller.go:131","msg":"Failed to prepare Ops Manager connection: Error reading or creating project in Ops Manager: Error reading all groups for user \"jason.mimick\" in Ops Manager: Status: 403 (Forbidden), ErrorCode: IP_ADDRESS_NOT_ON_WHITELIST, Detail: IP address 76.246.93.324 is not allowed to access this resource.",
```

After a few minutes, you should be able to see you new MongoDB replica set

#### Test the database connection

As a bonus step, let's try and test connecting to the database we just deployed.
That's is afterall why you've gone through all this.

One way to test connectivity is to use the mongo shell. For this, we need a
connection string. In order to build this connection string in the
`mongodb+srv://` format, we need to figure out the DNS name for the internal
ClusterIP service created for our replica set via the operator.

The following snippet finds the name of this internal service, launches a pod to
run a host command in to query the native cluster DNS for SRV records and see
how they are mapped to the actual pod's running the MongoDB replica set.

```bash
➜  kubectl get services
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
hello-db-svc            ClusterIP   None            <none>        27017/TCP         33m
hello-db-svc-external   NodePort    10.101.80.243   <none>        27017:30654/TCP   33m
➜  kubectl run dnstester --restart=Never --image=tutum/dnsutils --  host -t srv hello-db-svc
pod/dnstester created
➜  kubectl get pods
NAME                                           READY   STATUS      RESTARTS   AGE
dnstester                                      0/1     Completed   0          5m12s
hello-db-0                                     1/1     Running     0          40s
hello-db-1                                     1/1     Running     0          83s
hello-db-2                                     1/1     Running     0          2m
mongodb-enterprise-operator-5c9c9b764b-vlqcc   1/1     Running     0          43m
➜  kubectl logs dnstester
hello-db-svc.mongodb.svc.cluster.local has SRV record 0 50 27017 hello-db-0.hello-db-svc.mongodb.svc.cluster.local.
hello-db-svc.mongodb.svc.cluster.local has SRV record 0 50 27017 hello-db-2.hello-db-svc.mongodb.svc.cluster.local.
```

to test connection:

```bash
kubectl run mongo-test --restart=Never --image=jmimick/simple-mongodb-connection-tester hello-db-svc.mongodb.svc.cluster.local
kubectl logs mongo-test

<INSERT LOG OUTPUT HERE>
```

clean up testing pods:

```bash
kubectl delete pod {dnstester,mongo-test}
```

### GCE

## Production Notes
[inject general production notes, deployment blueprints]

### Prod notes

#### Using existing Persistent Volumes for MongoDB deployments

By default, the Operator will dynamically generate a Persistent Volume Claim
(PVC) for each MongoDB database pod. This allows the storage for your MongoDB
deployments to be managed in a standard Kubernetes-way. The `podSpec` field in a
given MongoDB deployment yaml allows one to configure the details on the PVC's
created by the operator. For example, consider the following snippet:

```yaml
spec:
  ...
  podSepc:
    storage: 20Gi
    storageClass: dbproduction
```

This will add a request of 20 gigabytes of storage from the "dbproduction"
storage class provider. Cluster admins should pre-provision PersistentVolumes
of the correct storage class which sasisify the storage requirements prior to
deploying a MongoDB cluster. Note, there is usually a default storage class
which can be used. To do so, simply omit any reference to the storage class in
the `podSpec` and persistent volume definition.

Here is a more complicated example which configures different PVC's for each
type of storage per MongoDB container, data, logs, and
[journal](https://docs.mongodb.com/manual/core/journaling/). Note the additional
use of a `labelSelctor` for the journal mount.

```yaml
spec:
  ...
  podSpec:
    persistence:
      multiple:
        data:
          storage: 10Gi
        journal:
          storage: 1Gi
          labelSelector:
            matchLabels:
              app: "my-app"
        logs:
          storage: 500M
          storageClass: standard
```


Also see:
- [Create a Persistent Volume](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume). 

- [samples/extended/replica-set.yaml](https://github.com/mongodb/mongodb-enterprise-kubernetes/blob/1d00e0da57f2d9f6ce4c4cda9f41cfaa95df4998/samples/extended/replica-set.yaml#L28)


### Deployment Blueprints

##### Basic 3-Node Replica Set

##### Microservice

##### MDBaaS

### Namespace Considerations

## Containerizing MongoDB Ops Manager


## Resources


| What | Where |
| ---- | ----- |
| Source repository for mdb-k8s-op artifacts | https://github.com/mongodb/mongodb-enterprise-kubernetes |
| Container repository with mdb-k8s operator images | https://quay.io/organization/mongodb |
| Official Installation Documentation | https://docs.opsmanager.mongodb.com/current/tutorial/install-k8s-operator/ |
| Troubleshooting | https://docs.opsmanager.mongodb.com/current/reference/troubleshooting/k8s/ |
| Webinars | <TODO> |
| Blogs | https://blog.openshift.com/mongodb-kubernetes-operator/<br/>https://www.mongodb.com/blog/post/introducing-mongodb-enterprise-operator-for-kubernetes-openshift<br/>https://hackernoon.com/getting-started-with-mongodb-enterprise-operator-for-kubernetes-bb5d5205fe02
|






Index



