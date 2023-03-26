#!/bin/bash

set -o errexit
set -o nounset

celery -A app.app.celery_app beat -l DEBUG --max-interval 86400