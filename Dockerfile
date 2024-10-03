# Pull base image
FROM python:3.9-slim-bookworm as builder

# install python project dependencies pre-requisites
RUN apt-get update && \
    apt-get install -y libldap2-dev libsasl2-dev libssl-dev && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config

# Copy Pipfile dependency list
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi


FROM builder as final
WORKDIR /code
COPY . . 

RUN set -ex && bash -c "eval $(grep 'PYTHONDONTWRITEBYTECODE' .env)"
RUN set -ex && bash -c "eval $(grep 'PYTHONUNBUFFERED' .env)"
