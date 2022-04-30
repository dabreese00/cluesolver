test:
	poetry run pytest cluesolver/tests/unit

cov:
	poetry run coverage run -m pytest cluesolver/tests/unit
	poetry run coverage report

cov_all:
	poetry run coverage run -m pytest
	poetry run coverage report

cov_html:
	poetry run coverage html

test_int:
	poetry run pytest cluesolver/tests/integration

test_all:
	poetry run pytest

rundev:
	poetry run flask run

init_db:
	poetry run flask init-db
