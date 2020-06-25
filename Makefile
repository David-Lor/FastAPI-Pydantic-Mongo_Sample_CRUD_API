.DEFAULT_GOAL := help

install-requirements: ## pip install requirements for app
	pip install -r requirements.txt

install-test-requirements: ## pip install requirements for tests
	pip install -r requirements-test.txt

install-all-requirements: ## pip install requirements for app & tests
	make install-requirements
	make install-test-requirements

test: ## run tests
	pytest -sv .

run: ## python run app
	python .

run-docker: ## start running through docker-compose
	docker-compose up

run-docker-background: ## start running through docker-compose, detached
	docker-compose up -d

teardown-docker: ## remove from docker through docker-compose
	docker-compose down

start-test-mongo: ## start mongodb in docker for tests
	docker run -d --rm --name=fastapi_mongodb_tests -p 27017:27017 --tmpfs=/data/db mongo

stop-test-mongo: ## stop dockerized mongodb for tests
	docker stop fastapi_mongodb_tests

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
