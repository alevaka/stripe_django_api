# stripe_django_api
### Тестовое задание

### Запуск в Docker
```
git clone https://github.com/alevaka/stripe_django_api.git
cd stripe_django_api/stripe_api
# Создать файл с переменными среды (пример ниже)
touch .env
docker compose up -d
docker compose exec web python3 manage.py createsuperuser
```
### Пример заполнения .env
```
STRIPE_API_PUBLIC_KEY=pk_test_VOOyyYjgzqdm8I3SrBqmh9qY
DJANGO_SECRET_KEY=GdMGD6HNQ_qdgxYP8yBZAdAIV1w
DJANGO_DEBUG_STATUS=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```