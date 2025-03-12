#!/bin/bash
set -e  # Arrête le script si une commande échoue

# Variables
RESOURCE_GROUP="kaassiRG"                   # Nom du groupe de ressources
CONTAINER_GROUP_NAME="django-app-group"     # Nom du groupe de conteneurs
ACR_NAME="kaassiregistry"                     # Nom de l'Azure Container Registry
REGION="francecentral"                        # Région de déploiement
DOCKER_COMPOSE_FILE="docker-compose.yml"      # Nom de votre fichier docker-compose
DJANGO_IMAGE_NAME="bamk-django"                # Nom local de l'image Django
NGINX_IMAGE_NAME="bamk-nginx"                  # Nom local de l'image Nginx
DNS_LABEL="bamkapp"                            # Label DNS pour accéder au groupe de conteneurs

# Charger les variables d'environnement (par exemple SECRET_KEY, DATABASE_URL, etc.)
. ./.env

echo "REGISTRY_USERNAME from .env (si défini): $REGISTRY_USERNAME"
echo "REGISTRY_PASSWORD from .env (si défini): $REGISTRY_PASSWORD"

# 1. Authentification Azure (assurez-vous d'être connecté via 'az login')
echo "Authentification Azure..."
# az login

# 2. Connexion à Azure Container Registry
echo "Connexion à Azure Container Registry..."
az acr login --name $ACR_NAME
az acr update -n $ACR_NAME --admin-enabled true
REGISTRY_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
REGISTRY_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# 3. Suppression de l'ancien groupe de conteneurs (s'il existe)
echo "Suppression du groupe de conteneurs existant (le cas échéant)..."
az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_GROUP_NAME --yes

# 4. Construction des images Docker avec docker-compose
echo "Construction des images Docker via docker-compose..."
docker-compose -f $DOCKER_COMPOSE_FILE build

# 5. Taguer les images pour ACR
echo "Taguer l'image Django..."
docker tag $DJANGO_IMAGE_NAME $ACR_NAME.azurecr.io/$DJANGO_IMAGE_NAME:latest
echo "Taguer l'image Nginx..."
docker tag $NGINX_IMAGE_NAME $ACR_NAME.azurecr.io/$NGINX_IMAGE_NAME:latest

# 6. Pousser les images vers ACR
echo "Pousser l'image Django vers ACR..."
docker push $ACR_NAME.azurecr.io/$DJANGO_IMAGE_NAME:latest
echo "Pousser l'image Nginx vers ACR..."
docker push $ACR_NAME.azurecr.io/$NGINX_IMAGE_NAME:latest

# 7. Création d'un fichier YAML pour le groupe de conteneurs multi-conteneurs
echo "Création du fichier YAML de déploiement pour le groupe de conteneurs..."
cat > aci-deploy.yaml <<EOF
apiVersion: 2019-12-01
location: ${REGION}
name: ${CONTAINER_GROUP_NAME}
properties:
  containers:
  - name: django
    properties:
      image: ${ACR_NAME}.azurecr.io/${DJANGO_IMAGE_NAME}:latest
      resources:
        requests:
          cpu: 1.0
          memoryInGb: 3.5
      environmentVariables:
      - name: SECRET_KEY
        value: "${SECRET_KEY}"
      - name: DATABASE_URL
        value: "${DATABASE_URL}"
      - name: ACCESS_TOKEN_EXPIRE_MINUTES
        value: "${ACCESS_TOKEN_EXPIRE_MINUTES}"
      - name: ALGORITHM
        value: "${ALGORITHM}"
      - name: MODEL_PATH
        value: "${MODEL_PATH}"
      ports:
      - port: 8080
  - name: nginx
    properties:
      image: ${ACR_NAME}.azurecr.io/${NGINX_IMAGE_NAME}:latest
      resources:
        requests:
          cpu: 0.5
          memoryInGb: 1.0
      ports:
      - port: 80
  osType: Linux
  ipAddress:
    type: Public
    dnsNameLabel: ${DNS_LABEL}
    ports:
    - protocol: tcp
      port: 8080
  imageRegistryCredentials:
  - server: ${ACR_NAME}.azurecr.io
    username: ${REGISTRY_USERNAME}
    password: ${REGISTRY_PASSWORD}
EOF

# 8. Déploiement du groupe de conteneurs sur Azure Container Instances
echo "Déploiement du groupe de conteneurs sur Azure Container Instances..."
az container create --resource-group $RESOURCE_GROUP --file aci-deploy.yaml

# 9. Afficher l'URL d'accès du groupe de conteneurs
CONTAINER_FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_GROUP_NAME --query "ipAddress.fqdn" -o tsv)
echo "Le groupe de conteneurs est déployé. Vous pouvez y accéder à l'adresse suivante : http://${CONTAINER_FQDN}"
