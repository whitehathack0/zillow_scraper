# Zillow Scraper
This repo contains code for a simple zillow scraper celery task that hit zillows 
API and pulls new houses in Boston around certain filters. This data is then inserted 
in a postgres RDS database.

#### How to run locally:
- install requirements via requirements.txt
- Ensure RDS postgres DB is running
- Run each in different terminal window:
  - Run Redis via `docker pull redis`
  - Run Celery worker via `celery -A app.app.celery_app worker -l DEBUG`
  - Run Celery beat via `celery -A app.app.celery_app beat -l DEBUG`