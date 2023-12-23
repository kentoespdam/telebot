.PHONY: build
build:
	@echo "Building..."
	docker compose -f docker/docker-compose.yml build

.PHONY: start
start:
	@echo "Starting..."
	docker compose -f docker/docker-compose.yml up -d

.PHONY: stop
stop:
	@echo "Stopping..."
	docker compose -f docker/docker-compose.yml down