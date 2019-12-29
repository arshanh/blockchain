SHELL = /bin/bash
USER := $(shell id -un)
PWD := $(shell pwd)

IMAGE_NAME = blockchain
IMAGE_TAG = $(shell cat Dockerfile | shasum | awk '{print substr($$1,0,11);}')

# Build and tag at hash of Dockerfile
DOCKER_BUILD = docker build --no-cache \
               -t $(IMAGE_NAME) . && \
               docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

DOCKER_RUN := docker run --rm=true -p 8080:80 -d\

.PHONY: blockchain blockchain-bash
.DEFAULT_GOAL := blockchain

blockchain:
	@docker inspect --type image $(IMAGE_NAME):$(IMAGE_TAG) &> /dev/null || \
	{ echo Image $(IMAGE_NAME):$(IMAGE_TAG) not found. Building... ; \
	$(DOCKER_BUILD) ; }
	$(DOCKER_RUN) -t $(IMAGE_NAME):$(IMAGE_TAG)

