from celery import Celery
from celery.schedules import crontab
from flask import Flask


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    return app


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    celery.conf.timezone = 'America/New_York'
    celery.conf.beat_schedule = {
        'scrape-every-minute': {
            'task': 'app.tasks.scraper',
            'schedule': crontab(minute='5', hour='16', day_of_week='*', day_of_month='*', month_of_year='*'),
        },
    }

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = create_celery_app()
