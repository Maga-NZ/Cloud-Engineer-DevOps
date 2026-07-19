.DEFAULT_GOAL := help
COMPOSE := docker compose

.PHONY: help up down build restart logs ps test lint fmt health deploy tf-init tf-plan tf-apply ansible clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

up: ## Start the full stack in the background
	$(COMPOSE) up -d

down: ## Stop and remove the stack
	$(COMPOSE) down

build: ## Build the application image
	$(COMPOSE) build

restart: down up ## Restart the stack

logs: ## Follow logs (use SERVICE=app to scope)
	$(COMPOSE) logs -f $(SERVICE)

ps: ## Show container status
	$(COMPOSE) ps

test: ## Run the test suite
	python -m pytest tests/ -v

lint: ## Lint Python code
	flake8 python/ tests/ docker/app --count --select=E9,F63,F7,F82 --show-source --statistics

fmt: ## Format Terraform files
	cd terraform && terraform fmt -recursive

health: ## Run a one-shot health check
	python python/monitoring/health_check.py --once

deploy: ## Run the deployment script (ENV=dev|staging|prod)
	python python/deployment/deploy.py --environment $(or $(ENV),dev)

tf-init: ## terraform init
	cd terraform && terraform init

tf-plan: ## terraform plan
	cd terraform && terraform plan

tf-apply: ## terraform apply
	cd terraform && terraform apply

ansible: ## Run the Ansible playbook
	cd ansible && ansible-playbook -i inventory/hosts.yml playbooks/main.yml

clean: ## Stop the stack and remove volumes
	$(COMPOSE) down -v
