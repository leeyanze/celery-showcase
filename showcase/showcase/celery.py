import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showcase.settings")

'''
Segregation - for heavy tasks only
'''
heavy_app = Celery("showcase_heavy")
heavy_app.config_from_object("django.conf:settings", namespace="CELERY")

heavy_app.conf.imports = ("showcase.heavy_tasks",)

heavy_app.conf.task_queues = [
    Queue("heavy", Exchange("heavy"), routing_key="heavy.run"),
    Queue("light", Exchange("light"), routing_key="light.run"),  # publisher needs to know it
]
heavy_app.conf.task_default_queue = "heavy" # if you want a default queue
heavy_app.conf.task_routes = {
    "showcase.heavy_tasks.heavy_task":  {"queue": "heavy", "routing_key": "heavy.run"},
    "showcase.light_tasks.light_task":  {"queue": "light", "routing_key": "light.run"}, 
}
heavy_app.conf.worker_prefetch_multiplier = 1  # Sensible defaults for heavy tasks - one task at a time, no prefetch

'''
Segregation - for light tasks only
'''
light_app = Celery("showcase_light")
light_app.config_from_object("django.conf:settings", namespace="CELERY")
light_app.conf.imports = ("showcase.light_tasks",)
light_app.conf.task_queues = [
    Queue("light", Exchange("light"), routing_key="light.run"),
    Queue("heavy", Exchange("heavy"), routing_key="heavy.run"),  # publisher needs to know it
]
light_app.conf.task_default_queue = "light" # if you want a default queue
light_app.conf.task_routes = {
    "showcase.light_tasks.light_task":  {"queue": "light", "routing_key": "light.run"},
    "showcase.heavy_tasks.heavy_task":  {"queue": "heavy", "routing_key": "heavy.run"}, 
}

'''
Publisher / beat app that knows BOTH task modules
'''
publisher_app = Celery("showcase")
publisher_app.config_from_object("django.conf:settings", namespace="CELERY")
publisher_app.conf.imports = ("showcase.heavy_tasks", "showcase.light_tasks")
publisher_app.conf.task_queues = [
    Queue("heavy", Exchange("heavy"), routing_key="heavy.run"),
    Queue("light", Exchange("light"), routing_key="light.run"),
]
publisher_app.conf.task_routes = {
    "showcase.heavy_tasks.heavy_task": {"queue": "heavy", "routing_key": "heavy.run"},
    "showcase.light_tasks.light_task": {"queue": "light", "routing_key": "light.run"},
}