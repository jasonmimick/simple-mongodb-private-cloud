# DISCLAIMER

this project is currently in-flight
it is merely a demonstration of a concept

The MongoDB Open Service Broker is the go-to place for deploying
Enterprise-grade data services in your cloud-native environments. The broker is
compliant with version 2.XX of the
[openbrokerapi](https://openbrokerapi.readthedocs.io/) and currently offers
support for the following MongoDB Ssrvices:

- MongoDB Ops Manager
- MongoDB Kubernetes Operator
- DBaaS w/ above & starter deplyment templates (t-shirts)

we expect to support at some point:

- MongoDB Atlas
- MongoDB BI-Connector
- MongoDB Charts
- MongoDB Stitch
- Mongomart
- ...?

* demo notes *

ripped of from openbrokerapi skeleton

implementation details-

- single, simple deployment with python script which attempts to implements the
  k8s api through the python kube-client
- flask app
  - auth: specially named secret is mmounted
  - supervisord pattern like operator
  - broker/broker.py
  - `broker/templates` is a special directory where the various templates for
    service plans are installed.
  - since the broker - `catalog()` API returns a list of "Plans", the idea is
    that each "service provider" claims a name (or "id") in the
`broker/templates/<service_provider_name>` directory by convention
  - the broker will then dynamically load all the plans.
  - for each service provider, each plan should be given a fixed name in
    `broker/templates/<service_provider_name>/<plan_id>
  - each plan folder can contain .yaml or .url using Jinja templates


# OpenBrokerAPI Skeleton

Basic skeleton to implement a service broker with [openbrokerapi](https://openbrokerapi.readthedocs.io/)

## What to implement

| Feature                 | Method           |
|-------------------------|------------------|
| Register service broker | `catalog`        |
| Visible in marketplace  | `catalog`        |
| Create service          | `provision`      |
| Bind service            | `bind`           |
| Unbind service          | `unbind`         |
| Delete service          | `deprovision`    |
| Support async           | `last_operation` |



## Deploy on Cloud Foundry

```bash

# deploy
cf push --random-route

# register service broker in space
cf create-service-broker [broker name] [username] [password] [url] --space-scoped

```

