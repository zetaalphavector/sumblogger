SHELL:=/bin/bash
.PHONY: help install-dev run dev test dev-test linter check-types unit-tests \\
	integration-tests coverage clean-build clean-pyc clean-test clean test-ci \\
	unit-tests-ci integration-tests-ci prod build-prod install-prod


dry_run = true

help:
	@echo "clean - remove all artifacts"	
	@echo "clean-build - remove Python build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test artifacts"
	@echo "install-prod - installs production dependencies"
	@echo "prod - creates a docker environment for production"
	@echo "build-prod - builds the docker image for production"
	@echo "install-dev - installs test/dev dependencies"
	@echo "dev - creates a docker environment for development"
	@echo "build-dev - builds the docker image for development"
	@echo "test - runs all tests"
	@echo "dev-test - runs all tests inside a docker environment and exits"
	@echo "linter - runs linter"
	@echo "check-types - checks type correctness"
	@echo "unit-tests - runs unit tests"
	@echo "integration-tests - runs integration tests"
	@echo "coverage - runs coverage"
	@echo "requirements-prod - updates production dependencies"
	@echo "requirements-dev - updates test/dev dependencies"
	@echo "requirements - updates all dependencies"

clean: clean-build clean-pyc clean-test

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
	uv pip install --no-deps -r requirements/prod.txt
build-prod:
	docker buildx build --platform linux/amd64 -f Dockerfile -t sumblogger .
prod: build-prod
	docker-compose -f docker-compose-prod.yml up -d
	-docker exec -it sumblogger_api_1 /bin/bash
	docker-compose down

install-dev:
	uv pip install --no-deps -r requirements/dev.txt
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
coverage:
	coverage report

requirements-prod:
	uv pip compile requirements/prod.in -o requirements/prod.txt
	sed -i '' -E "s/-e file:\/\/\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/prod.txt 2>/dev/null || true
requirements-dev:
	uv pip compile requirements/dev.in -o requirements/dev.txt
	sed -i '' -E "s/-e file:\/\/\/.*\/sumblogger\/(.*)/-e .\/\1/g" requirements/dev.txt 2>/dev/null || true

requirements: requirements-prod requirements-dev