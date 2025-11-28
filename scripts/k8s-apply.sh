#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Iniciando despliegue en Kubernetes...${NC}"

echo "Aplicando Namespace..."
kubectl apply -f k8s/namespace.yaml

echo "Aplicando Configuración y Secretos..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

echo "Desplegando Aplicación y Servicio..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo -e "${GREEN}Despliegue completado exitosamente.${NC}"
echo "Verifica el estado de los pods con: kubectl get pods -n config-rotator"
