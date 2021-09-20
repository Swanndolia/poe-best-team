# Malt scraper, mongoBD and mongo-express on kubernetes

## Prerequisite

Docker installed and running
Minikube installed on MacOs or linux

## Installation

Start minikube:

```zsh
minikube start
````

minikube dashboard activation (useful to monitor minikube)

```zsh
minikube addons enable dashboard
minikube addons enable metrics-server
````

To get the URL

```zsh
minikube dashboard --url
````

Set the folder with the yml files as working directory. In the terminal windows type the following commands

```zsh
kubectl apply -f ./namespace.yml
kubectl apply -f ./configmap.yml
kubectl apply -f ./secret.yml
kubectl apply -f ./mongo.stateful.yml
kubectl apply -f ./mongo-express.deployment.yml
kubectl apply -f ./scraper_malt.deployment.yml
kubectl apply -f ./mongo.service.yml
kubectl apply -f ./mongo-express.service.yml
kubectl apply -f ./ingress.yml
minikube addons enable ingress
minikube service -n mongo-namespace mongo-express-service --url 

```
or run the exec file


## Usage

Scrap the website https://www.malt.fr/ and return the results as JSON files. The search criteria are :
- CSS
- JAVA
- JS
- python

The JSON files are stored in a malt database in 4 collections : Java, js, python and CSS.
Mongodb is monitored trought mongo-express :
    localhost:8081

