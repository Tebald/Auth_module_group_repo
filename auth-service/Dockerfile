FROM python:3.11-slim as base

WORKDIR /app
ENV PATH /app/.venv/bin/:$PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir


FROM base AS prod

COPY --from=base /app /app
COPY src ./src
COPY  main.py .


ENTRYPOINT [ "gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker ", "--bind", "0.0.0.0:8000" ]


FROM base as tests

COPY --from=base /app /app
COPY src ./src

ENV PYTHONPATH /app
RUN chmod 774 /app/src/tests/functional/utils/tests_entrypoint.sh

ENTRYPOINT [ "/app/src/tests/functional/utils/tests_entrypoint.sh" ]

