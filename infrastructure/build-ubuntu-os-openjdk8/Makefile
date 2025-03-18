.DEFAULT_GOAL := help
include ../.env

IMAGE_NAME=ubuntu-openjdk8
VERSION=24.04

define HELP

Available commands:

- build: Build this project

endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help

build:  
	docker build --build-arg REPO_NAME=${REPO_NAME} -t ${REPO_NAME}/${IMAGE_NAME}:${VERSION} .
