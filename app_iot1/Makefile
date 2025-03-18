.DEFAULT_GOAL := help
include ../devlab/.env

IMAGE_NAME=iot_datagen
VERSION=3.0

define HELP

Available commands:

- build: Build the Python IoT Datagen App

endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help

build:
	docker build -t ${REPO_NAME}/${IMAGE_NAME}:${VERSION} .

