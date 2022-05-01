unit:
	poetry run pytest cluesolver/tests/unit

cov:
	poetry run coverage run -m pytest
	poetry run coverage report

cov_html:
	poetry run coverage html

integration:
	poetry run pytest cluesolver/tests/integration

test_all:
	poetry run pytest

rundev:
	poetry run flask run

init_db:
	poetry run flask init-db
