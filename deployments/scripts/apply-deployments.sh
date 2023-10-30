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
# Prometheus/Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus --namespace prometheus --create-namespace prometheus-community/kube-prometheus-stack 
# rabbit
helm install my-release oci://registry-1.docker.io/bitnamicharts/rabbitmq --set auth.username="guest" --set auth.password="guest"
