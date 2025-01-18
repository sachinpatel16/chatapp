import os

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# env = os.getenv('DJANGO_ENV', 'development')  # Default to development
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{env}')

app = Celery('chatapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# app.conf.update(
#     worker_concurrency=1,
#     worker_force_execv=True,
#     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# )

app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    broker_connection_retry=True,  # Current behavior
    broker_connection_retry_on_startup=True,  # New setting for Celery 6.0+
)
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')