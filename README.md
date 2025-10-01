# celery-showcase
## Setup virtualenv and install packages
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## To spinup dependent services (RabbitMQ, Postgres)
```
docker-compose up -d
```

## For django database setup
```
cd showcase
python manage.py migrate
```

## Run celery showcase 
```
# to see 2 different worker pools where one manages heavy tasks, one manages light tasks; also shows 10 heavy tasks chaining into light tasks
python manage.py celery_tutorial
```

## View makefile functions
```
cat Makefile
```


## For running django and creating superuser to go into django admin
```
python manage.py createsuperuser
python manage.py runserver 
# then navigate to localhost:8000/admin
# useful for demonstrating celery beat periodic task
```
