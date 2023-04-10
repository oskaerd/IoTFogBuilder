# Kafka
kubectl apply -f kafka/kafka-namespace.yaml
kubectl apply -f kafka/zookeeper.yaml
kubectl apply -f kafka/kafka.yaml
# CouchDB
kubectl apply -f couchdb/couchdb-namespace.yaml
kubectl apply -f couchdb/couchdb-secret.yaml
kubectl apply -f couchdb/couchdb.yaml
# NodeRED
kubectl apply -f node-red/node-red-namespace.yaml
kubectl apply -f node-red/node-red.yaml