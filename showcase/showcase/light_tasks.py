from .celery import light_app

# sample values are tuned for light tasks that should succeed eventually
# 
@light_app.task(
    bind=True,
    autoretry_for=(Exception,),          # auto-retry on ANY exception
    retry_backoff=True,                  # 1s, 2s, 4s, 8s, ...
    retry_jitter=True,                   # add randomness to avoid thundering herd
    retry_kwargs={"max_retries": None},  # <-- unlimited retries
    retry_backoff_max=60                # set higher for light tasks (can afford to wait more)
)
def light_task(self, msg: str):
    # do work here; raise to test retries
    # if something_bad(msg): raise RuntimeError("transient")
    return f"light got: {msg}"


# sample values are tuned for periodic tasks that  are non critical and will be re-ran periodically by beats anyway
@light_app.task(
    bind=True,
    autoretry_for=(Exception,),          # auto-retry on ANY exception
    retry_backoff=True,                  # 1s, 2s, 4s, 8s, ...
    retry_jitter=True,                   # add randomness to avoid thundering herd
    # retry_kwargs={"max_retries": 3},  # <-- max retries default is 3
    retry_backoff_max=600                # set as default
)
def periodic_task(self):
    return f"periodic task ran"