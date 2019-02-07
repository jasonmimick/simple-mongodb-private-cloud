FROM openjdk:8-jdk

ENV GRADLE_HOME /opt/gradle
ENV GRADLE_VERSION 4.4

ARG GRADLE_DOWNLOAD_SHA256=d717e46200d1359893f891dab047fdab98784143ac76861b53c50dbd03b44fd4
RUN set -o errexit -o nounset \
	&& echo "Downloading Gradle" \
	&& wget --no-verbose --output-document=gradle.zip "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" \
	\
	&& echo "Installing Gradle" \
	&& unzip gradle.zip \
	&& rm gradle.zip \
	&& mv "gradle-${GRADLE_VERSION}" "${GRADLE_HOME}/" \
	&& ln --symbolic "${GRADLE_HOME}/bin/gradle" /usr/bin/gradle \
	\
	&& echo "Adding gradle user and group" \
	&& groupadd --system --gid 1000 gradle \
	&& useradd --system --gid gradle --uid 1000 --shell /bin/bash --create-home gradle \
	&& mkdir /home/gradle/.gradle \
	&& chown --recursive gradle:gradle /home/gradle

COPY . /spring
WORKDIR /spring

EXPOSE 8080

RUN /spring/gradlew clean assemble

COPY run.sh /run.sh

#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/run.sh"]

#ENTRYPOINT [ "java", "-jar", "build/libs/spring-music.jar", "-Dspring.profiles.active=mongodb" ]
#CMD java -jar -Dlogging.level.org.hibernate=DEBUG -Dspring.profiles.active="mongodb" -Dspring.data.mongodb.uri="mongodb://docker:MongoDB123@docker-shard-00-00-1cihx.gcp.mongodb.net:27017,docker-shard-00-01-1cihx.gcp.mongodb.net:27017,docker-shard-00-02-1cihx.gcp.mongodb.net:27017/test?ssl=true&replicaSet=docker-shard-0&authSource=admin&retryWrites=true" build/libs/spring-music.jar
