.PHONY: setup dev build test lint deploy rollback clean help

setup: ## Install all dependencies and pull Docker images
	pnpm install
	docker-compose pull
	@echo "\n✅ Setup complete. Run 'make dev' to start."

dev: ## Start all services in development mode
	docker-compose up -d
	@echo "Waiting for PostgreSQL..."
	@sleep 3
	$(MAKE) db-migrate
	pnpm -r --parallel dev

build: ## Build all packages
	pnpm -r build

test: ## Run all tests
	pnpm -r test

lint: ## Run linting
	pnpm -r lint

db-migrate: ## Run database migrations
	cd packages/api && alembic upgrade head

db-seed: ## Seed database with sample data
	tsx scripts/seed-db.ts

db-shell: ## Connect to PostgreSQL shell
	docker-compose exec postgres psql -U golden_hour golden_hour

redis-shell: ## Connect to Redis CLI
	docker-compose exec redis redis-cli

docker-build: ## Build production Docker images
	docker build -f Dockerfile.api -t golden-hour-api:latest .
	docker build -f Dockerfile.dashboard -t golden-hour-dashboard:latest .

deploy: ## Deploy to production
	bash scripts/deploy.sh

rollback: ## Rollback to previous deployment
	bash scripts/rollback.sh

backup: ## Backup database
	bash scripts/backup-db.sh

clean: ## Stop all services and remove volumes
	docker-compose down -v
	pnpm -r exec rm -rf dist build .next node_modules

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
