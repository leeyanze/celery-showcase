RABBITMQ_CONTAINER = rabbitmq
CELERY      := celery
APP         := showcase.celery:publisher_app
SCHEDULER   := django            # DatabaseScheduler
PIDFILE     := .celerybeat.pid

.PHONY: queues clear_queues status heavy_workers light_workers beat beat_bg beat_stop beat_status

# List all queues
queues:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmqctl list_queues name messages consumers

clear_queues:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmqctl purge_queue celery

# Show node status
status:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmq-diagnostics status

# Run Celery heavy_tasks worker pool
heavy_workers:
	celery -A showcase.celery:heavy_app worker -l info -Q heavy

# Run Celery heavy_tasks worker pool
light_workers:
	celery -A showcase.celery:light_app worker -l info -Q light

# Run in foreground (good for demos)
beat:
	$(CELERY) -A $(APP) beat -l info -S $(SCHEDULER)

# Run as a daemon
beat_bg:
	$(CELERY) -A $(APP) beat -l info -S $(SCHEDULER) --detach --pidfile=$(PIDFILE)

# Stop the daemon (if started with beat_bg)
beat_stop:
	- test -f $(PIDFILE) && kill `cat $(PIDFILE)` || echo "No beat pidfile"

# Quick check it's running
beat_status:
	ps aux | grep 'celery.*beat' | grep -v grep || true