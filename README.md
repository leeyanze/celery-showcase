# celery-showcase

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

docker-compose up -d


cd showcase
python manage.py migrate


python manage.py celery_tutorial