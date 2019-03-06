simple connection tester
======

This repo has a simple docker container which is 
intended to be used to test MongoDB clusters
deployed on Kubernetes clusters.

The simple test container accepts one argument, a valid MongoDB connection
string. 

A sample `Pod` definition for Kubernetes is available in
[simple-mongodb-connection-tester.yaml](simple-mongodb-connection-tester.yaml). 
In this demonstration, our application
"pod" contains deployment logic to mount a Kubernetes Secret as and environment
variable which is then passed along as an argument to the container runtime.

For [istio](ist.io) users, a basic `ServiceEntry` definition is available in
[simple-istio-mongodb-egress.yaml](simple-istio-mongodb-egress.yaml). When attempting to connect to MongoDB
clusters running outside your isto-enabled Kubernetes environments such a
configuration is neccessary. In this example, we're defining the hostnames for
each node in the target MongoDB cluster.

```yaml
  hosts:
  - docker-shard-00-00-1cihx.gcp.mongodb.net
  - docker-shard-00-01-1cihx.gcp.mongodb.net
  - docker-shard-00-02-1cihx.gcp.mongodb.net 
```

For users running MongoDB 3.6 or greater things are even easier since we can
collapse the detailed hostname info for each MongoDB replicaset node for the
logical DNS SRV hostname. See
[simple-istio-mongodb-egress-srv.yaml](simple-istio-mongodb-egress-srv.yaml).

Out ServiceEntry is only:

```yaml
  hosts:
  - docker-1cihx.gcp.mongodb.net
```

and the secret containing the connection string is:

```
kubectl create secret generic simple-mongodb-connection-tester \
--from-literal=mongodburi="mongodb+srv://XXX:XXX@docker-1cihx.gcp.mongodb.net/test?retryWrites=true"
```

From the logs of the connection-tester container we can see how under the
covers, the DNS magic is resolving `docker-1cihx.gcp.mongodb.net` to the
multiple `docker-shard-00-0*` hostnames. This reduces the direct dependency
between the tolopogy of your database clusters and your applications.


```
# logs from 
#kubectl logs -f simple-mongodb-connection-test -c connection-tester
simple-connection-test: testing connection to mongodb+srv://docker:MongoDB123@docker-1cihx.gcp.mongodb.net/test?retryWrites=true
Creating and reading 100 docs in the 'test-3195cae8.foo' namespace
Database(MongoClient(host=['docker-shard-00-02-1cihx.gcp.mongodb.net:27017', 'docker-shard-00-00-1cihx.gcp.mongodb.net:27017', 'docker-shard-00-01-1cihx.gcp.mongodb.net:27017'], document_class=dict, tz_aware=False, connect=True, ssl=True, retrywrites=True, replicaset=u'docker-shard-0', authsource=u'admin'), u'test-3195cae8')
```


