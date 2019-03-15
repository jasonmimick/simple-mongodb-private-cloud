FROM anapsix/alpine-java
ARG YCSB_VERSION=0.15.0
# Kudos to: MAINTAINER dianaesteves
MAINTAINER jasonmimick

# exposed port -- spells YCSB in a dial pad :)
EXPOSE 9272 

RUN apk update && apk add --update curl python ca-certificates && cd /opt && curl -OL https://github.com/brianfrankcooper/YCSB/releases/download/${YCSB_VERSION}/ycsb-${YCSB_VERSION}.tar.gz

RUN cd /opt && tar xvf /opt/ycsb-${YCSB_VERSION}.tar.gz && ls -Rl /opt && mv /opt/ycsb-${YCSB_VERSION} /opt/ycsb

COPY ./ycsb-entrypoint.sh /opt

ENTRYPOINT ["opt/ycsb-entrypoint.sh"]
#CMD ["tail", "-f", "/dev/null"]


