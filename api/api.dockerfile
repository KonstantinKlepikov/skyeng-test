FROM python:3.10.6

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y git curl && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./app /app
COPY ./api-start.sh /api-start.sh
WORKDIR /app
ENV PYTHONPATH=/app

RUN bash -c "poetry install"

RUN chmod +x /api-start.sh

CMD ["bash", "/api-start.sh"]
