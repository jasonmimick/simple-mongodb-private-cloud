FROM anapsix/alpine-java
ARG YCSB_VERSION=0.15.0
ARG POCDRIVER_JAR=./POCDriver
# Kudos to: MAINTAINER dianaesteves
MAINTAINER jasonmimick

COPY ./POCDriver.jar /POCDriver.jar
ENTRYPOINT [ "java", "-jar", "/POCDriver.jar" ]
