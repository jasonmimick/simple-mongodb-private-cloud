#!/bin/bash

CONNECTION_STRING=$1

az container create -g ops-manager-cloudfoundry --name ycsb --image nullstring/alpine-ycsb --memory 2 --cpu 1 --command-line "/opt/ycsb-0.10.0/bin/ycsb load mongodb -P workloads/workloada -p mongodb.url=${CONNECTION_STRING}"

