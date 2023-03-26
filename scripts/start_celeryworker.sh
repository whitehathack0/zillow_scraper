#!/bin/bash

set -o errexit
set -o nounset

celery -A app.app.celery_app worker -l DEBUG