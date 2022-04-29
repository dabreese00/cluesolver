test:
	poetry run pytest


cov:
	poetry run coverage run -m pytest
	poetry run coverage report


cov_html:
	poetry run coverage html
