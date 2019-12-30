SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = blockchain
IMAGE_TAG = $(shell cat Dockerfile src/* requirements.txt | shasum | awk '{print substr($$1,0,11);}')

# Build and tag at hash of files
DOCKER_BUILD = docker build \
               -t $(IMAGE_NAME) . && \
               docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

DOCKER_RUN := docker run --rm=true -p 8080:80\

.PHONY: run-detach run-attach ps stop
.DEFAULT_GOAL := run-detach

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
shell:
	docker exec -it $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}") bash

# Stop container
stop:
	docker stop $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):latest --format="{{.ID}}")

