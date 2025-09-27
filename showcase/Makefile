RABBITMQ_CONTAINER = rabbitmq

.PHONY: queues clear_queues status heavy_workers light_workers beat

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
	celery -A showcase.celery:heavy_app worker -l info -Q heavy -Ofair

# Run Celery heavy_tasks worker pool
light_workers:
	celery -A showcase.celery:light_app worker -l info -Q light

# Run Celery beat scheduler
beat:
	celery -A showcase beat -l info

# Run Heavy worker pool