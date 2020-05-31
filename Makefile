CURRENT_DIR = $(shell pwd)
DOCKER_NAME = helios
DOCKER_RUN  = docker run \
							--name $(DOCKER_NAME) \
							-p7474:7474 -p7687:7687 \
							-d \
							-v $(CURRENT_DIR)/neo4j/data:/data \
							-v $(CURRENT_DIR)/neo4j/logs:/logs \
							-v $(CURRENT_DIR)/neo4j/import:/var/lib/neo4j/import \
							-v $(CURRENT_DIR)/neo4j/plugins:/plugins \
							--env NEO4J_AUTH=neo4j/test \
							$(DOCKER_NAME)

##
## Project
##-----------

build: ## Build the container
	@docker build -t $(DOCKER_NAME) $(CURRENT_DIR) --no-cache

start: ## Start the project
	@$(DOCKER_RUN)

stop: ## Stop the project
	@docker stop $(DOCKER_NAME)

clean: ## Remove the container use for the project
	@docker rm $(DOCKER_NAME)

bash: ## Access to the container throught /bin/bash
	@$(EXEC) /bin/bash

.PHONY: build bash start stop

# rules based on files
.DEFAULT_GOAL := help
help:
	@grep -E '(^[%a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-25s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
