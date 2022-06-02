FROM python:3.10-alpine AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev zlib-dev jpeg-dev
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install