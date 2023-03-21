# Zillow Scraper
This repo contains code for a simple zillow scraper celery task that hit zillows 
API and pulls new houses in Boston around certain filters. This data is then inserted 
in a postgres RDS dataase. Currently Celery task is set to run every day at 9am EST.

#### How to run locally:
- install requirements via requirements.txt
- Run each in different terminal window:
  - Run Redis via `./redis-3.2.1/src/redis-server`
  - Run Celery worker via `celery worker -A app.celery --loglevel=INFO`
  - Run Celery beat via `celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid`