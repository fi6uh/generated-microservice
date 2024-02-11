.PHONY: all build run clean create-network

# Docker container names
UI_CONTAINER_NAME = ui-container
MIDDLEWARE_CONTAINER_NAME = middleware-container
DB_CONTAINER_NAME = postgres-container

# Docker network name
NETWORK_NAME = my-network

# IPs
UI_IP = 172.18.0.6
MIDDLEWARE_IP = 172.18.0.5
DB_IP = 172.18.0.4

# Ports
UI_PORT = 8080
MIDDLEWARE_PORT = 5150
DB_PORT = 5432

all: build run

build:
	@echo "Building Docker containers..."
	@docker build -t $(UI_CONTAINER_NAME) ui/
	@docker build -t $(MIDDLEWARE_CONTAINER_NAME) middleware/
	@docker build -t $(DB_CONTAINER_NAME) postgres/

create-network:
	@echo "Creating Docker network..."
	@docker network create --subnet=172.18.0.0/16 $(NETWORK_NAME)

run-ui: create-network
	@echo "Running UI container..."
	@docker run --rm -d -p $(UI_PORT):$(UI_PORT) --network=$(NETWORK_NAME)  --ip=$(UI_IP) --name $(UI_CONTAINER_NAME) $(UI_CONTAINER_NAME)

run-middleware: create-network
	@echo "Running Middleware container..."
	@docker run --rm -d -p $(MIDDLEWARE_PORT):$(MIDDLEWARE_PORT) --network=$(NETWORK_NAME) --ip=$(MIDDLEWARE_IP) --name $(MIDDLEWARE_CONTAINER_NAME) $(MIDDLEWARE_CONTAINER_NAME)

run-db: create-network
	@echo "Running PostgreSQL container..."
	@docker run --rm -d -p $(DB_PORT):$(DB_PORT) --network=$(NETWORK_NAME) --ip=$(DB_IP) --name $(DB_CONTAINER_NAME) $(DB_CONTAINER_NAME)

run: run-ui run-middleware run-db

clean:
	@echo "Stopping and removing Docker containers..."
	@docker stop $(UI_CONTAINER_NAME) $(MIDDLEWARE_CONTAINER_NAME) $(DB_CONTAINER_NAME) || true
	@docker rm $(UI_CONTAINER_NAME) $(MIDDLEWARE_CONTAINER_NAME) $(DB_CONTAINER_NAME) || true
	@echo "Removing Docker network..."
	@docker network rm $(NETWORK_NAME) || true
