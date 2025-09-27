from .celery import heavy_app
from celery import Task
import time, random

class HeavyBase(Task):
    # Auto-retry with backoff; good for flaky heavy jobs
    autoretry_for = (Exception,)
    retry_backoff = True    # 2^retries seconds
    retry_backoff_max = 60
    retry_jitter = True     # introduces some randomness to retry delay
    max_retries = 3         # set lower for heavy tasks to avoid clogging queue

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print("RETRYING", self.name, task_id, self.request.retries, self.max_retries, {"exc": str(exc)})
        return super().on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("FAILURE TODO DEADLETTER QUEUE", self.name, task_id, self.request.retries, self.max_retries, {"exc": str(exc)})
        return super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        print("SUCCESS(DONT RECORD IN PROD BECAUSE NOISY)", self.name, task_id, self.request.retries, self.max_retries, {"retval": str(retval)})
        return super().on_success(retval, task_id, args, kwargs)

@heavy_app.task(
    bind=True, base=HeavyBase, acks_late=True
)
def heavy_task(self, seconds: int):
    time.sleep(seconds)
    if random.random() < 0.3:
        raise RuntimeError("simulated heavy failure")
    return f"heavy done in {seconds}s"
