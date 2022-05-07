FROM python:3.10 as base

WORKDIR /app


FROM base as builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13
RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt


FROM base as final

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
COPY --from=builder /app/requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./

ENV FLASK_APP=cluesolver/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
