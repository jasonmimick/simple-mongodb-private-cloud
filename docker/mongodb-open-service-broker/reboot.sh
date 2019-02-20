#!/bin/bash
docker stop osbmdb && docker rm osbmdb
docker build -t jmimick/mongodb-open-service-broker .
docker run -d --name osbmdb -p 5000:5000 jmimick/mongodb-open-service-broker
sleep 5
docker logs osbmdb
