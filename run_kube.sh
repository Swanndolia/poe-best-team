minikube delete --all
minikube start
minikube addons enable ingress
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
kubectl apply -f ./ingress.yml
kubectl apply -f ./namespace.yml
kubectl apply -f ./configmap.yml
kubectl apply -f ./secret.yml
python3 ./programatic_scheduled_jobs/__main__.py