build up:
	docker-compose up -d --build

up:
	docker-compose up -d

migrate:
	docker-compose exec api bash -c "python manage.py migrate"

celery:
	docker-compose exec api bash -c "celery -A src worker -B -l info"

test:
	docker-compose exec api bash -c "python manage.py test"

down:
	docker-compose down 