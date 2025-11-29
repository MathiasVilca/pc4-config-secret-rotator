SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.PHONY: setup test build scan tunnel dev rotate-config rotate-secret smoke help

REQUIREMENTS_PATH="app/requirements.txt"
IMAGE_NAME?=pc4-config-secret-rotator

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r $(REQUIREMENTS_PATH)

test: setup
	@echo "Ejecutando tests..."
	. .venv/bin/activate && pytest tests

build:
	@if [ -z "$(TAG)" ]; then echo "Error: set TAG variable (e.g. make build TAG=v1.0.0)"; exit 2; fi
	@if [ "$(TAG)" = "latest" ]; then echo "Error: use an explicit tag, not 'latest'"; exit 2; fi
	@echo "Construyendo imagen $(IMAGE_NAME):$(TAG) usando Dockerfile..."
	docker build --pull -t $(IMAGE_NAME):$(TAG) -f Dockerfile .

scan:
	@if command -v trivy >/dev/null 2>&1; then \
		trivy image --severity CRITICAL,HIGH --no-progress $(IMAGE_NAME):$(TAG); \
	else \
		echo "Scan placeholder: instala 'trivy' para realizar un escaneo real (https://github.com/aquasecurity/trivy)"; \
	fi

sbom:
	@if [ -z "$(TAG)" ]; then echo "Error: set TAG variable"; exit 2; fi
	@if ! command -v trivy >/dev/null 2>&1; then \
		echo "Sbom placeholder: instala 'trivy' para realizar un escaneo real (https://github.com/aquasecurity/trivy)"; \
		exit 1; \
	fi
	@echo "Creando directorio de evidencias..."
	mkdir -p evidence
	
	@echo "Generando SBOM para $(IMAGE_NAME):$(TAG)..."
	trivy image --format cyclonedx --output evidence/sbom.json --no-progress $(IMAGE_NAME):$(TAG)
	
	@echo "SBOM generado exitosamente en 'evidence/sbom.json'"

tunnel:
	@echo "Iniciando túnel en puerto 8000... (Presiona Ctrl+C para detener)"
	kubectl port-forward svc/config-rotator-service -n config-rotator 8000:80

rotate-secret:
	@echo "Rotando secretos..."
	./scripts/k8s-rotate-secret.sh
	@echo "Secretos rotados! Ejecute 'make tunnel' para volverse a conectar!"

rotate-config:
	@echo "Rotando configuración..."
	@echo "Uso: make rotate-config ARGS='--app_mode=Prod --log_level=DEBUG --max_retries=5'"
	./scripts/k8s-rotate-config.sh $(ARGS)
	@echo "Configuración rotada! Ejecute 'make tunnel' para volverse a conectar!"

smoke:
	@echo "Ejecutando prueba de humo (Smoke Test)..."
	./scripts/k8s-smoke.sh

dev:
	minikube start
	eval $$(minikube docker-env) && make build TAG=v1.0.0
	./scripts/k8s-apply.sh
	kubectl wait --for=condition=ready pod -l app=config-rotator -n config-rotator --timeout=60s || true
	@echo "Entorno listo, ahora ejecute 'make tunnel' para conectarse."

reset:
	@echo "Destruyendo entorno para iniciar desde cero..."
	minikube delete
	@echo "Entorno limpio. Puede ejecutar 'make dev'"

help:
	@echo "====== TARGETS DISPONIBLES ======"
	@echo ""
	@echo "Desarrollo:"
	@echo "  make dev    - Inicia minikube, construye imagen y despliega app"
	@echo "  make tunnel - Inicia port-forward para acceder a la app (8000:80)"
	@echo ""
	@echo "Build y Scan:"
	@echo "  make setup         - Configura entorno Python (venv + dependencies)"
	@echo "  make test          - Ejecuta tests"
	@echo "  make build TAG=<v> - Construye imagen Docker"
	@echo "  make scan          - Escanea imagen con Trivy (si está instalado)"
	@echo ""
	@echo "Rotación de Configuración y Secretos:"
	@echo "  make rotate-config ARGS='--app_mode=Prod --log_level=DEBUG --max_retries=5 --target_system="modern-db"'"
	@echo "                                      - Rota config con parámetros personalizados"
	@echo "  make rotate-secret                  - Rota secretos usando script"
	@echo "  make smoke                          - Ejecuta smoke test"
	@echo ""
	@echo "Mantenimiento:"
	@echo "  make reset         - Destruye minikube (limpia todo)"
	@echo "  make help          - Muestra esta ayuda"