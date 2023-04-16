# Applies all listed deployments. No input arguments.
# Example usage:
#   ./apply-deployments.sh
# Kafka
kubectl apply -f ../kafka/kafka-namespace.yaml
kubectl apply -f ../kafka/zookeeper.yaml
kubectl apply -f ../kafka/kafka.yaml
kubectl apply -f ../kafka/kafdrop.yaml
# CouchDB
kubectl apply -f ../couchdb/couchdb-namespace.yaml
kubectl apply -f ../couchdb/couchdb-secret.yaml
kubectl apply -f ../couchdb/couchdb.yaml
# NodeRED
kubectl apply -f ../node-red/node-red-namespace.yaml
kubectl apply -f ../node-red/node-red.yaml
# Grafana
kubectl apply -f ../grafana/grafana-namespace.yaml
kubectl apply -f ../grafana/grafana.yaml