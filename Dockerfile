FROM python:3.10-alpine AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev zlib-dev jpeg-dev
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install

# ---

FROM python:3.10-alpine
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

RUN adduser app -h /app -u 1000 -g 1000 -DH
USER 1000

# CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0,0,0,0", "--port", "80"]