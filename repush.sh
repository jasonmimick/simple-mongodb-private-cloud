#!/bin/bash
cd docker/mongodb-open-service-broker/
docker build -t jmimick/mongodb-open-service-broker .
docker push jmimick/mongodb-open-service-broker 
cd ../..
