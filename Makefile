CURRENT_DIR = $(shell pwd)
DOCKER_NAME = helios
DOCKER_RUN  = docker run \
							-it\
							--rm \
							--name $(DOCKER_NAME) \
							-p127.0.0.1:7474:7474 -p127.0.0.1:7687:7687 \
							-p127.0.0.1:80:8000 \
							-d \
							-v $(CURRENT_DIR)/src:/app \
							-v $(CURRENT_DIR)/neo4j/data:/data \
							-v $(CURRENT_DIR)/neo4j/logs:/logs \
							-v $(CURRENT_DIR)/neo4j/import:/var/lib/neo4j/import \
							-v $(CURRENT_DIR)/neo4j/plugins:/plugins \
							--env NEO4J_AUTH=none \
							--env AWS_ACCESS_KEY_ID="$(AWS_ACCESS_KEY_ID)" \
							--env AWS_SECRET_ACCESS_KEY="$(AWS_SECRET_ACCESS_KEY)" \
							$(DOCKER_NAME)

# Get AWS credential 
AWS_ACCESS_KEY_ID     = $$(aws configure get aws_access_key_id --profile corp)
AWS_SECRET_ACCESS_KEY = $$(aws configure get aws_secret_access_key --profile corp)

# Some shortcut
DOCKER_EXEC = docker exec -it $(DOCKER_NAME) /bin/bash -c 
ERASE_DATA = $(DOCKER_EXEC) "python3 erase.py"
ENV = default
##
## Management Command
##------------------------------

setup: ## /!\ Copy your ~/.aws/credentials into a directoy gitignored /!\ 
	@ cp ~/.aws/credentials conf/credentials

build: ## Build the container
	@docker build -t $(DOCKER_NAME) $(CURRENT_DIR) --no-cache

start: ## Start the container
	@$(DOCKER_RUN) && docker ps -a
	@$(DOCKER_EXEC) "sleep 15 && python3 collect.py dev"

stop: ## Clean the DB and stop the container
	@docker stop $(DOCKER_NAME)

clean: ## Remove all the data
	@rm -fr neo4j

##
## Project Command 
##------------------------------

refresh: ## Refresh all data
	@$(ERASE_DATA)
	@$(DOCKER_EXEC) "python3 collect.py -p ${ENV} -v"

cmap: ## Cloud Mapper with a DNS in entrypoint
	@$(ERASE_DATA)
	@$(DOCKER_EXEC) "python3 cmap.py ${ENV} ${DNS}"

##
## Debug Command
##------------------------------

bash: ## Access to the container throught /bin/bash
	@docker exec -it $(DOCKER_NAME) /bin/bash

debug: ## Launch script to test the connection with neo4j database
	@$(DOCKER_EXEC) "python3 test/neo4j_connect.py"

.PHONY: build start stop refresh cmap clean bash

# rules based on files
.DEFAULT_GOAL := help
help:
	@grep -E '(^[%a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-15s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
