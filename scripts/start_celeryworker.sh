#!/bin/bash

set -o errexit
set -o nounset

celery worker -A app.celery --loglevel=INFO