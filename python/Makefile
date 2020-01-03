SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = block-node
SERVICE_NAME = blockchain
NET_NAME = net-blockchain
STACK_NAME = onechain
COMPOSE_FILE = docker-compose.yml # used by docker stack
IMAGE_TAG = $(shell find . \( \
			  -name '*.py' -o \
			  -name 'Dockerfile' -o \
			  -name 'requirements.txt' -o \
			  -name 'docker-compose.yml' \) -exec cat {} \; | \
			  shasum | awk '{print substr($$1,0,11);}')

# Only used with swarm commands. Replicas for stacks set in compose file
REPLICAS = 5

# Build and tag at hash of files
DOCKER_BUILD = docker build \
               -t $(IMAGE_NAME) . && \
               docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

DOCKER_RUN := docker run --rm=true -p 8080:80\

.PHONY: run-detach run-attach ps stop
.DEFAULT_GOAL := run-detach

#######################################################################
# Single Container targets
#######################################################################

# Build if files have changed, Run in detached mode, non-interactive
# Use this if you just want to run in background
run-detach:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -d -t $(IMAGE_NAME):$(IMAGE_TAG)

# Build if files have changed, run and attach to contianer, non-interactive
# Use this if you want to see stdout
run-attach:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG)

# Same as run-attach but with interactive mode
# Use this if you want to use pdb
run-debug:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -it $(IMAGE_NAME):$(IMAGE_TAG)

# Get id of container running latest image
ps:
	docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}"

# Attach to stdout of container
attach:
	docker attach $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}")

# Exec a shell in the container
# This uses "head -n 1" so that if you are running a swarm it works as well
# But obviously it will only ssh into the first container returned by docker -ps
shell:
	docker exec -it $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}" | head -n 1) bash

# Stop container
# If you rebuild using any of the above commands before stopping an old container this target 
# will no longer work as both the hash and the latest tag have changed
stop:
	docker stop $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}")

#######################################################################
# Docker Stack 
#######################################################################

# Deploy using docker stack 
# Currently have to add/remove network manually because it is declared as external
# But we only have to do this because we want to access the network
# from outside of the stack.
stack:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	docker network create --driver overlay --attachable $(NET_NAME)
	docker stack deploy --compose-file $(COMPOSE_FILE) $(STACK_NAME)

# Clean using docker stack 
stack-clean:
	docker stack rm $(STACK_NAME) 
	docker network rm $(NET_NAME)

#######################################################################
# Docker Swarm (use stack instead)
#######################################################################

# OLD WAY: Using only CLI (no docker compose)
swarm:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	docker network create --driver overlay --attachable $(NET_NAME)
	docker service create --replicas $(REPLICAS) --endpoint-mode dnsrr --network $(NET_NAME) --name $(SERVICE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

# OLD WAY: Cleanup blockchain service and network using CLIs
swarm-clean:
	docker service rm $(SERVICE_NAME)
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
	docker run --network=$(NET_NAME) -it -v ~/projects/one-chain/python:/app python:3 bash

swarm-info: swarm-ls swarm-ps 

stack-info: stack-ps stack-ls

make logs:
	docker service logs $(STACK_NAME)_$(SERVICE_NAME)
