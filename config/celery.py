import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# Create the Celery app
app = Celery('ecommerce_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set Redis as the broker and result backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Set task serializer
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.result_serializer = 'json'

# Set task time limits
app.conf.task_time_limit = 60 * 5  # 5 minutes
app.conf.task_soft_time_limit = 60 * 3  # 3 minutes

# Configure periodic tasks
app.conf.beat_schedule = {
    'update-product-cache': {
        'task': 'apps.products.tasks.update_product_cache',
        'schedule': 60 * 10.0,  # every 10 minutes
    },
}
app.conf.update(
    worker_pool='solo'
)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')