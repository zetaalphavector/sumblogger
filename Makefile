SHELL:=/bin/bash
.PHONY: help install-dev run dev test dev-test linter check-types unit-tests \\
	integration-tests coverage clean-build clean-pyc clean-test clean test-ci \\
	unit-tests-ci integration-tests-ci prod build-prod install-prod


dry_run = true

help:
	@echo "install-dev - installs test/dev dependencies"
	@echo "run - runs the application"
	@echo "dev - creates a docker environment for development"
	@echo "test - runs all tests"
	@echo "dev-test - runs all tests inside a docker environment and exits"
	@echo "linter - runs linter"
	@echo "check-types - checks type correctness"
	@echo "unit-tests - runs unit tests"
	@echo "integration-tests - runs integration tests"
	@echo "coverage - runs coverage"
	@echo "clean-build - remove Python build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test artifacts"
	@echo "clean - remove all artifacts"
	@echo "test-ci - runs all tests in CI mode (no GUI)"
	@echo "unit-tests-ci - runs unit tests in CI mode"
	@echo "integration-tests-ci - runs integration tests in CI mode"
	@echo "prod - creates a docker environment for production"
	@echo "build-prod - builds the docker image for production"
	@echo "install-prod - installs production dependencies"

clean: clean-build clean-pyc clean-test

copy-zav-deps:
	rm -rf shared
	mkdir shared
	cp -r ../backend/shared/api ./shared
	cp -r ../backend/shared/message-bus ./shared
	cp -r ../backend/shared/logging ./shared
	cp -r ../backend/shared/domain-model-repo ./shared

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr tests/.pytest_cache/

install-prod:
	pip install --no-deps -r requirements/prod.txt
build-prod:
	docker buildx build --platform linux/amd64 -f Dockerfile -t sumblogger .
prod: build-prod
	docker-compose -f docker-compose-prod.yml up -d
	-docker exec -it sumblogger_api_1 /bin/bash
	docker-compose down

install-dev:
	pip install --no-deps -r requirements/dev.txt
build-dev:
	docker buildx build --platform linux/amd64 -f test.Dockerfile -t sumblogger .
dev: build-dev
	docker-compose up -d
	-docker exec -it sumblogger_api_1 /bin/bash
	docker-compose down
	
dev-test: build-dev
	docker-compose up -d
	-docker-compose exec sumblogger_api_1 make test
	docker-compose down
dev-test-ci:
	docker-compose up -d
	docker-compose exec -T sumblogger_api_1 make test-ci

test: clean linter check-types unit-tests integration-tests
test-ci: linter check-types unit-tests-ci integration-tests-ci
linter:
	flake8 src tests
check-types:
	mypy --install-types --enable-incomplete-features --non-interactive  src tests
unit-tests:
	set -a; . ./dev.env; set +a; \
	python -m pytest tests/unit/ --cov=src --cov-append -svvv --sw
integration-tests:
	set -a; . ./dev.env; set +a; \
	python -m pytest tests/integration/ --cov=src --cov-append -svvv --sw
unit-tests-ci:
	python -m pytest tests/unit/ --cov=src --cov-append -svvv
integration-tests-ci:
	python -m pytest tests/integration/ --cov=src --cov-append -svvv
coverage:
	coverage report

requirements-prod:
	pip-compile --no-emit-index-url requirements/prod.in
	sed -i '' -E "s/-e file:\/\/\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/prod.txt
	sed -i '' -E "s/zav\..* @ file:\/\/localhost\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/prod.txt
requirements-dev:
	pip-compile --no-emit-index-url -q requirements/dev.in
	sed -i '' -E "s/-e file:\/\/\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/dev.txt
	sed -i '' -E "s/zav\..* @ file:\/\/localhost\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/dev.txt

requirements: requirements-prod requirements-dev