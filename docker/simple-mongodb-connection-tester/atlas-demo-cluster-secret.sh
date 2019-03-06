kubectl create secret generic simple-mongodb-connection-tester --from-literal=mongodburi="mongodb://docker:MongoDB123@docker-shard-00-00-1cihx.gcp.mongodb.net:27017,docker-shard-00-01-1cihx.gcp.mongodb.net:27017,docker-shard-00-02-1cihx.gcp.mongodb.net:27017/admin?ssl=true&replicaSet=docker-shard-0&authSource=admin&retryWrites=true"


kubectl create secret generic simple-mongodb-connection-tester --from-literal=mongodburi="mongodb+srv://docker:MongoDB123@docker-1cihx.gcp.mongodb.net/test?retryWrites=true"
