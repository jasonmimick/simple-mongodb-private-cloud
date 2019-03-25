#!/bin/bash
set -x
PARAMS=$(cat <<END
{ "service_id": "mongodb-open-service-broker",
  "plan_id": "standard-mongodb-replset",
  "context": {
    "version": "4.0.0",
    "namespace": "mongodb" },
  "organization_guid": "sample mongodb paremeters",
  "space_guid": "no spaces",
  "parameters": {
    "members" : 3,
    "project" : "minimom",
    "credentials" : "minimom",
    "cpu" : "0.5",
    "memory" : "500M" } }
END
)

echo "${PARAMS}"

svcat provision broker-rs1 --class mongodb-open-service-broker-service --plan \
standard-mongodb-replset --params-json $(echo "${PARAMS}") 
