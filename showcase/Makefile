RABBITMQ_CONTAINER = rabbitmq
CELERY      := celery
APP         := showcase.celery:publisher_app
SCHEDULER   := django            # DatabaseScheduler
PIDFILE     := .celerybeat.pid

.PHONY: queues clear_queues status heavy_workers light_workers beat beat_bg beat_stop beat_status flower

queues:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmqctl list_queues name messages consumers

clear_queues:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmqctl purge_queue celery

status:
	docker exec -it $(RABBITMQ_CONTAINER) rabbitmq-diagnostics status

heavy_workers:
	celery -A showcase.celery:heavy_app worker -l info -Q heavy

light_workers:
	celery -A showcase.celery:light_app worker -l info -Q light

beat:
	$(CELERY) -A $(APP) beat -l info -S $(SCHEDULER)

beat_bg:
	$(CELERY) -A $(APP) beat -l info -S $(SCHEDULER) --detach --pidfile=$(PIDFILE)

beat_stop:
	- test -f $(PIDFILE) && kill `cat $(PIDFILE)` || echo "No beat pidfile"

beat_status:
	ps aux | grep 'celery.*beat' | grep -v grep || true

flower_heavy:
	celery -A showcase.celery:heavy_app flower --port=5001