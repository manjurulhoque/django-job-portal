ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
include $(ROOT_DIR)/.mk-lib/common.mk

.PHONY: help start serve test stop restart status ps clean purge build

start: ## Start all or c=<name> containers in FOREGROUND
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c)

serve: ## Start all or c=<name> containers in BACKGROUND
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c) -d

test: ## Execute tests
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) run --rm  --entrypoint "invoke test" test

# start: ## Start all or c=<name> containers in background
# 	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d $(c)

stop: ## Stop all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)

restart: ## Restart all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) restart $(c)

status: ## Show status of containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

ps: status ## Alias of status

clean: confirm ## Clean all containers (keeping volumes)
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

purge: confirm ## Purge all containers and volumes
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v

build: ## (re)Build all images or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build $(c)