#!/bin/sh
if [ -z "$1" ]
  then
    if [ -z "${MONGODB_URI}" ]
      then
        echo "No MongoDB connection string specified. Pass as argument"
        echo "Please use:"
        echo "docker run jmimick/spring-music <MONGODB_CONNECTION_STRING>"
        exit 1
    fi
    echo "No args, but detected env MONGODB_URI='${MONGODB_URI}'"
  else 
   MONGODB_URI=${1}
fi

echo "Launching Spring Music connecting to ${MONGODB_URI}"

SPRING_MUSIC_JAR="/spring/build/libs/spring-music.jar"
#java -jar -Dlogging.level.org.hibernate=DEBUG -Dspring.profiles.active="mongodb" -Dspring.data.mongodb.uri="${MONGODB_URI}" ${SPRING_MUSIC_JAR}
java -jar -Dspring.profiles.active=mongodb -Dspring.datasource.url="${MONGODB_URI}" -Dspring.data.mongodb.uri="${MONGODB_URI}" ${SPRING_MUSIC_JAR}
