.PHONY: setup test

REQUIREMENTS_PATH="app/requirements.txt"

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r $(REQUIREMENTS_PATH)

test: setup
	@echo "Ejecutando tests..."
	. .venv/bin/activate && pytest tests
