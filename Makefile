.PHONY: setup test build scan deploy

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

deploy:
	@echo "Aplicando configuraciones..."
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/service.yaml
	@echo "Calculando checksum de la configuración..."
	$(eval CONFIG_CHECKSUM := $(shell python3 -c "import hashlib; print(hashlib.sha256(open('k8s/configmap.yaml', 'rb').read()).hexdigest())"))
	@echo "Checksum: $(CONFIG_CHECKSUM)"
	@echo "Aplicando Deployment con anotación de checksum..."
	kubectl apply -f k8s/deployment.yaml
	kubectl patch deployment config-rotator-app -n config-rotator -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"checksum/config\":\"$(CONFIG_CHECKSUM)\"}}}}}"
	kubectl rollout status deployment/config-rotator-app -n config-rotator


dev:
	minikube start
	eval $$(minikube docker-env) && make build TAG=v1.0.0
	./scripts/k8s-apply.sh
	kubectl wait --for=condition=ready pod -l app=config-rotator -n config-rotator --timeout=60s || true
	kubectl port-forward svc/config-rotator-service -n config-rotator 8000:80 > /dev/null 2>&1 & \
	PID=$$!
	@echo "Tunel creado exitosamente, verificar en: http://localhost:8000/config"

reset:
	@echo "Destruyendo entorno para iniciar desde cero..."
	minikube delete
	@echo "Entorno limpio. Puede ejecutar 'make dev'"