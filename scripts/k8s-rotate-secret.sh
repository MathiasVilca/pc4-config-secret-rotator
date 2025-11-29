#!/bin/bash
set -euo pipefail

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando rotación de secretos...${NC}"

# 1. Ejecutar herramienta Python para generar y aplicar nuevos secretos
echo "Ejecutando tools/rotate_secret.py..."
if python3 tools/rotate_secret.py; then
    echo -e "${GREEN}Secretos rotados y aplicados exitosamente.${NC}"
else
    echo -e "${RED}ERROR: Falló la rotación de secretos.${NC}"
    exit 1
fi

echo "Reiniciando Pods para cargar el nuevo secreto..."
kubectl rollout restart deployment/config-rotator-app -n config-rotator

echo "Esperando despliegue exitoso..."
kubectl rollout status deployment/config-rotator-app -n config-rotator --timeout=60s

# 2. Ejecutar Smoke Test para validar
echo "Ejecutando validación (Smoke Test)..."
if ./scripts/k8s-smoke.sh; then
    echo -e "${GREEN}Validación exitosa. El sistema está operativo.${NC}"
else
    echo -e "${RED}ERROR: La validación falló tras la rotación.${NC}"
    exit 1
fi

echo -e "${GREEN}Proceso de rotación de secretos completado correctamente.${NC}"