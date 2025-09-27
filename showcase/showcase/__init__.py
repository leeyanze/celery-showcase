# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import heavy_app, light_app

__all__ = (heavy_app, light_app,)