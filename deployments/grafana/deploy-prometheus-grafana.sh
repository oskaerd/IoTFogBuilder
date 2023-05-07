helm install prometheus --namespace prometheus --create-namespace prometheus-community/kube-prometheus-stack 
echo
echo
echo "########### Now run:###########"
echo "kubectl edit service prometheus-grafana"
echo "And change service type from ClusterIp to NodePort"
echo "And set nodePort to desired exposed port"