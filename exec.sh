kubectl apply -f ./namespace.yml
kubectl apply -f ./configmap.yml
kubectl apply -f ./secret.yml
kubectl apply -f ./mongo.stateful.yml
kubectl apply -f ./mongo-express.deployment.yml
kubectl apply -f ./scraper-malt.deployment.yml
minikube addons enable ingress
kubectl apply -f ./ingress.yml
minikube service -n mongo-namespace mongo-express-service --url 