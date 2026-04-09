PYTHON=python
PIP=pip
UVI=uvicorn

.PHONY: help install test docker-build docker-run train quality-gate terraform-init

help:
	@echo "Available targets:"
	@echo "  install        Install python dependencies"
	@echo "  test           Run pytest validation suite"
	@echo "  train          Train a candidate model with MLflow"
	@echo "  quality-gate   Execute the challenger quality gate"
	@echo "  docker-build   Build the production Docker image"
	@echo "  docker-run     Run the service locally in Docker"
	@echo "  terraform-init Initialize Terraform configuration"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	pytest tests

train:
	$(PYTHON) src/training/train.py --model-name production-model --artifact-path model

quality-gate:
	if [ -z "$$RUN_ID" ]; then echo "RUN_ID environment variable is required"; exit 1; fi
	$(PYTHON) src/governance/quality_gate.py --run-id "$$RUN_ID" --artifact-path model

docker-build:
	docker build -t production-ml-lifecycle-platform:latest .

docker-run:
	docker run --rm -p 8000:8000 production-ml-lifecycle-platform:latest

terraform-init:
	cd terraform && terraform init
