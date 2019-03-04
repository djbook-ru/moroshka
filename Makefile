NAMESPACE = moroshka
PACKAGE = site
SOURCE_VERSION ?= $(shell cat VERSION)
SOURCE_COMMIT ?= $(shell git rev-parse --short=8 HEAD)
TAG = $(shell cat VERSION)
IMAGE_REGISTRY = registry.halfakop.ru:5000
IMAGE_PREFIX = $(NAMESPACE)/$(PACKAGE)
IMAGE_NAME_TAGGED = $(IMAGE_PREFIX):$(TAG)
IMAGE_NAME_LATEST = $(IMAGE_PREFIX):latest
CURDIR = $(shell pwd)
CACHEDIR ?= /tmp/$(PACKAGE)-cache
PORT ?= 8000

.EXPORT_ALL_VARIABLES:
	# this exports the following variables
	# see https://www.gnu.org/software/make/manual/make.html#index-_002eEXPORT_005fALL_005fVARIABLES

default: help

title:
	@echo "\Moroshka - The Company's Site\n"

help: title
	@echo "Usage: make {command}"
	@echo "    clean            clean the source code;"
	@echo "    run              run the application locally;"
	@echo "    rung             run the application as in production;"
	@echo "    bump             bump the version;"
	@echo
	@echo "    release          make the release;"
	@echo "      build          build the image;"
	@echo "      tags           tag the image;"
	@echo "      publish        publish the image;"
	@echo
	@echo "    test             run tests;"
	@echo
	@echo "Environment variables:"
	@echo "    SECRET_KEY       if undefined then restart of app drops session"
	@echo

clean:
	@find . -type d -name '__pycache__' -delete

bump:
	bumpversion --commit --tag patch

postgres_start:
	docker run --rm -d \
	  -l database \
	  --name postgres \
		-p 5432:5432 \
		postgres
		# -v postgres_data:/var/lib/postgresql/data/ \

postgres_stop:
	docker kill postgres

postgres_shell:
	psql -h $(DB_HOST) -p $(DB_PORT) -d $(DB_NAME) -U $(DB_USER)

postgres_dump:
	pg_dump -h $(DB_HOST) -p $(DB_PORT) \
		-U $(DB_USER) -C -Fc $(DB_NAME) -f backup_pgsql.gz

define run_variables
	SECRET_KEY=top_secret \
	PYTHONPATH=$(CURDIR)
endef

run:
	$(call run_variables) \
	python3 manage.py runserver

rung:
	$(call run_variables) \
	gunicorn -c gunicorn.py src.wsgi

shell:
	$(call run_variables) \
	python3 manage.py shell

dbshell:
	$(call run_variables) \
	python3 manage.py dbshell

release: clean build tags registry publish

build:
	$(eval SOURCE_VERSION := $(shell cat VERSION))
	$(eval SOURCE_COMMIT := $(shell git rev-parse HEAD))
	docker build \
		-t $(IMAGE_NAME_TAGGED) \
		-t $(IMAGE_NAME_LATEST) \
		--build-arg SOURCE_VERSION=$(SOURCE_VERSION) \
		--build-arg SOURCE_COMMIT=$(SOURCE_COMMIT) \
		-f Dockerfile .

tags:
	docker tag $(IMAGE_NAME_LATEST) $(IMAGE_REGISTRY)/$(IMAGE_NAME_LATEST)
	docker tag $(IMAGE_NAME_TAGGED) $(IMAGE_REGISTRY)/$(IMAGE_NAME_TAGGED)

registry:
	@echo ${DOCKER_PASSWORD} | \
	docker login -u ${DOCKER_USERNAME} --password-stdin $(IMAGE_REGISTRY)

publish:
	docker push $(IMAGE_REGISTRY)/$(IMAGE_NAME_LATEST)
	docker push $(IMAGE_REGISTRY)/$(IMAGE_NAME_TAGGED)

test:
	PYTHONPATH=. pytest
