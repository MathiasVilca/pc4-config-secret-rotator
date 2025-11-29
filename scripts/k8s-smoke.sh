#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

NAMESPACE="config-rotator"
SERVICE_NAME="config-rotator-service"
PORT=8081

echo -e "${GREEN}Iniciando Smoke Test...${NC}"

# Verificar si estamos dentro del cluster o fuera.

echo "Esperando a que el pod esté listo..."
kubectl wait --for=condition=ready pod -l app=config-rotator -n $NAMESPACE --timeout=60s >/dev/null

# Iniciar port-forward en background (registro temporal, no se muestra)
PF_LOG=$(mktemp)
kubectl port-forward svc/$SERVICE_NAME $PORT:80 -n $NAMESPACE >"$PF_LOG" 2>&1 &
PID=$!
trap 'kill ${PID} >/dev/null 2>&1 || true; rm -f "${PF_LOG}"' EXIT

# Esperar /health con reintentos
RETRY=0
MAX_RETRIES=30
SLEEP_SECONDS=1
HTTP_CODE=000
BODY=""
while [ $RETRY -lt $MAX_RETRIES ]; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 http://localhost:$PORT/health 2>/dev/null || echo 000)
    if [ "$HTTP_CODE" = "200" ]; then
        BODY=$(curl -s --max-time 2 http://localhost:$PORT/health 2>/dev/null || true)
        break
    fi
    sleep $SLEEP_SECONDS
    RETRY=$((RETRY+1))
done

if [ "$HTTP_CODE" = "200" ]; then
    echo "Smoke test: OK"
    # Verificar estructura mínima en /config
    CONFIG_BODY=$(curl -s --max-time 5 http://localhost:$PORT/config 2>/dev/null || true)
    echo "$CONFIG_BODY" | grep -q "config" >/dev/null 2>&1 || { echo "Smoke test: FAIL - /config inválido"; exit 1; }
    exit 0
else
    echo "Smoke test: FAIL - /health returned $HTTP_CODE"
    # show a small snippet of health body if any
    [ -n "$BODY" ] && echo "Health body: ${BODY:0:200}"
    rm -f "$PF_LOG"
    exit 1
fi
