#!/bin/bash
if [ -z "$1" ]
  then
    echo "No MongoDB connection string specified. Pass as argument"
fi
MONGODB_CONNECTION_STRING=$1

# Configure SSL if CA cert passed.
# pass contents of file on command line
if [ -z "$2" ]
  then
    CERT=${2}
    echo "Detected TSL Certificate. Attempting to install."
    echo ${CERT}
    echo ${CERT} > /usr/local/share/ca-certificates/cert.pem 
    ls -l /usr/local/share/ca-certificates
    update-ca-certificates
fi
echo "ycsb-entrypoint: mongodb.url=${MONGODB_CONNECTION_STRING}"
/opt/ycsb/bin/ycsb load mongodb -P /opt/ycsb/workloads/workloada -p mongodb.url="${MONGODB_CONNECTION_STRING}" 
