FROM python:3.10-slim-bullseye AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install

# ---

FROM python:3.10-slim-bullseye
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

RUN adduser app -h /app -u 1000 -g 1000 -DH
USER 1000

EXPOSE 8000
ENTRYPOINT [ "/app/.venv/bin/python" ]
CMD ["-m", "uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]