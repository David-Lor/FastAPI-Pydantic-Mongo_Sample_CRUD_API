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

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
