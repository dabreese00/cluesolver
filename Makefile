all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d app

test:
	poetry run pytest

unit:
	poetry run pytest tests/unit

down:
	docker-compose down

cov:
	poetry run coverage run -m pytest
	poetry run coverage report

cov_html:
	poetry run coverage html

rundev:
	poetry run flask run

tree:
	tree -I "__pycache__|htmlcov"
