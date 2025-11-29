#!/bin/bash
set -euo pipefail

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando rotación de configuración...${NC}"

# 1. Ejecutar herramienta Python para generar y aplicar nueva configuración
# Forwardear todos los parámetros recibidos por el script shell al script Python
echo "Ejecutando tools/rotate_config.py $*"
if python3 tools/rotate_config.py "$@"; then
    echo -e "${GREEN}Configuración rotada y aplicada exitosamente.${NC}"
else
    echo -e "${RED}ERROR: Falló la rotación de configuración.${NC}"
    exit 1
fi

# 1.5. Reiniciar el Deployment para que los Pods lean los nuevos valores
echo "Reiniciando Pods para aplicar cambios (Rollout Restart)..."
kubectl rollout restart deployment/config-rotator-app -n config-rotator

# ¡IMPORTANTE! Esperar a que el reinicio termine antes de probar
echo "Esperando a que los nuevos Pods estén listos..."
kubectl rollout status deployment/config-rotator-app -n config-rotator --timeout=60s

# 2. Ejecutar Smoke Test para validar
echo "Ejecutando validación (Smoke Test)..."
if ./scripts/k8s-smoke.sh; then
    echo -e "${GREEN}Validación exitosa. El sistema está operativo.${NC}"
else
    echo -e "${RED}ERROR: La validación falló tras la rotación.${NC}"
    exit 1
fi

echo -e "${GREEN}Proceso de rotación de configuración completado correctamente.${NC}"