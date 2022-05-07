unit:
	poetry run pytest tests/unit

integration:
	poetry run pytest tests/integration

e2e:
	poetry run pytest tests/e2e

test_all:
	poetry run pytest

cov:
	poetry run coverage run -m pytest
	poetry run coverage report

cov_html:
	poetry run coverage html

rundev:
	poetry run flask run

tree:
	tree -I "__pycache__|htmlcov"
