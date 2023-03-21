#!/bin/bash

set -o errexit
set -o nounset

celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid