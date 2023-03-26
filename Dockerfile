FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  && apt-get -qq -y install curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /app
COPY ./config /config

COPY ./scripts/start_celeryworker.sh /start_celeryworker.sh
RUN sed -i 's/\r$//g' /start_celeryworker.sh
RUN chmod +x /start_celeryworker.sh

COPY ./scripts/start_celerybeat.sh /start_celerybeat.sh
RUN sed -i 's/\r$//g' /start_celerybeat.sh
RUN chmod +x /start_celerybeat.sh

WORKDIR .