SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

NET_NAME = net-blockchain
STACK_NAME = onechain

# Build and tag at hash of files
DOCKER_BUILD = docker build \
               -t $(IMAGE_NAME) . && \
               docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

DOCKER_COMPOSE = docker-compose --project-directory $(PWD)

BLOCKCHAIN_COMPOSE = blockchain-compose.yml # used by docker stack
BLOCKNODE_COMPOSE = blocknode/blocknode-compose.yml
CLIENT_COMPOSE = client/client-compose.yml
SOURCE_COMPOSE = source/source-compose.yml

.PHONY: blocknode-detach 
.DEFAULT_GOAL := 


#######################################################################
# Build
#######################################################################
build-blocknode:
	$(DOCKER_COMPOSE) -f $(BLOCKNODE_COMPOSE) build

build-client:
	$(DOCKER_COMPOSE) -f $(CLIENT_COMPOSE) build

build-source:
	$(DOCKER_COMPOSE) -f $(SOURCE_COMPOSE) build

build:
	$(DOCKER_COMPOSE) -f $(BLOCKNODE_COMPOSE) \
				   -f $(CLIENT_COMPOSE) \
				   -f $(SOURCE_COMPOSE) build

#######################################################################
# Single Container targets
#######################################################################

# Use this if you just want to run in background
blocknode-detach:
	$(DOCKER_COMPOSE) -f $(BLOCKNODE_COMPOSE) up --detach

# Use this if you want to see stdout
blocknode-attach:
	$(DOCKER_COMPOSE) -f $(BLOCKNODE_COMPOSE) up

blocknode-down:
	$(DOCKER_COMPOSE) -f $(BLOCKNODE_COMPOSE) down

client-detach:
	$(DOCKER_COMPOSE) -f $(CLIENT_COMPOSE) up --detach

client-attach:
	$(DOCKER_COMPOSE) -f $(CLIENT_COMPOSE) up

client-down:
	$(DOCKER_COMPOSE) -f $(CLIENT_COMPOSE) down

source-detach:
	$(DOCKER_COMPOSE) -f $(SOURCE_COMPOSE) up --detach

source-attach:
	$(DOCKER_COMPOSE) -f $(SOURCE_COMPOSE) up

source-down:
	$(DOCKER_COMPOSE) -f $(SOURCE_COMPOSE) down

# If you need to run redis outside of swarm (for debugging)
redis:
	docker run --name my-redis -p 6379:6379 --restart always --detach redis

#######################################################################
# Docker Stack 
#######################################################################

# Deploy using docker stack 
# Currently have to add/remove network manually because it is declared as external
# But we only have to do this because we want to access the network
# from outside of the stack.
stack: build
	docker network create --driver overlay --attachable $(NET_NAME)
	docker stack deploy --compose-file $(BLOCKCHAIN_COMPOSE) $(STACK_NAME)

# Clean using docker stack 
stack-clean:
	docker stack rm $(STACK_NAME) 
	docker network rm $(NET_NAME)

#######################################################################
# Util
#######################################################################

swarm-ls:
	docker service ls

swarm-ps:
	docker service ps $(SERVICE_NAME)

stack-ls:
	docker stack ls

stack-ps:
	docker stack ps $(STACK_NAME)

# Run shell in network
# This only works for my director structure atm
test-shell:
	docker run --network=$(NET_NAME) -it -v \
		~/projects/one-chain/python:/app python:3 bash

swarm-info: swarm-ls swarm-ps 

stack-info: stack-ps stack-ls

blocknode-logs:
	docker service logs $(STACK_NAME)_blocknode
client-logs:
	docker service logs $(STACK_NAME)_client
source-logs:
	docker service logs $(STACK_NAME)_source

