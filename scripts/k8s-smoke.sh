#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

NAMESPACE="config-rotator"
SERVICE_NAME="config-rotator-service"
PORT=80

echo -e "${GREEN}Iniciando Smoke Test...${NC}"

# Verificar si estamos dentro del cluster o fuera.

echo "Esperando a que el pod esté listo..."
kubectl wait --for=condition=ready pod -l app=config-rotator -n $NAMESPACE --timeout=60s

echo "Estableciendo port-forward temporal para la prueba..."
kubectl port-forward svc/$SERVICE_NAME $PORT:80 -n $NAMESPACE > /dev/null 2>&1 &
PID=$!

trap "kill $PID" EXIT

sleep 2

echo "Realizando petición al endpoint /health..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/health)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}SUCCESS: La aplicación respondió con 200 OK.${NC}"
    
    echo "Verificando endpoint /config..."
    curl -s http://localhost:$PORT/config | grep "config" > /dev/null
    if [ $? -eq 0 ]; then
         echo -e "${GREEN}SUCCESS: Endpoint /config responde estructura válida.${NC}"
    else
         echo -e "${RED}ERROR: Endpoint /config no devolvió lo esperado.${NC}"
         exit 1
    fi

else
    echo -e "${RED}FAILURE: La aplicación respondió con código $HTTP_CODE.${NC}"
    exit 1
fi

echo -e "${GREEN}Smoke Test Finalizado Correctamente.${NC}"
