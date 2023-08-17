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
COPY ./worker-start.sh /worker-start.sh
WORKDIR /app
ENV PYTHONPATH=/app

RUN bash -c "poetry install"

# running celery as root
ENV C_FORCE_ROOT=1

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
