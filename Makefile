test:
	poetry run pytest cluesolver/tests/unit


cov:
	poetry run coverage run -m pytest cluesolver/tests/unit
	poetry run coverage report


cov_html:
	poetry run coverage html

test_int: init_db
	poetry run pytest cluesolver/tests/integration

test_all: test test_int

rundev:
	poetry run flask run

init_db:
	poetry run flask init-db
