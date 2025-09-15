# Foodgram - Кулинарное API

## Краткое описание проекта

Foodgram — это REST API для кулинарного приложения, которое позволяет пользователям:

- Создавать, редактировать и просматривать рецепты с ингредиентами и тегами.
- Добавлять рецепты в избранное и корзину покупок.
- Подписываться на других пользователей и просматривать их рецепты.
- Фильтровать рецепты по тегам и авторам.
- Загружать список ингредиентов из JSON-файла.
- Управлять пользователями и аутентификацией через Djoser.

Проект разработан для работы в контейнерах Docker с использованием PostgreSQL, Django REST Framework и Nginx.

## Стек технологий

- **Backend**: Python 3.11, Django, Django REST Framework, Djoser
- **Database**: PostgreSQL 15
- **Web Server**: Gunicorn, Nginx
- **Frontend**: Статические файлы (React)
- **Containerization**: Docker, Docker Compose
- **Дополнительно**: drf-base64 (для обработки изображений), django-filter (для фильтрации запросов)

## Как развернуть контейнеры на сервере

### Подготовьте сервер:

Установите Docker и Docker Compose:

```
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
```

Убедитесь, что порты 80 (или 7000, если используете другой) открыты.

### Склонируйте репозиторий:

```
git clone git@github.com:SharkFaceSF/foodgram.git
cd foodgram
```

### Создайте файл .env:

В корне проекта создайте файл `.env` с настройками:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

### Соберите и запустите контейнеры:

```
docker-compose up -d --build
```

### Примените миграции и импортируйте ингредиенты:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py import_ingredients
```

### Создайте суперпользователя:

```
docker-compose exec backend python manage.py createsuperuser
```

## Как запустить бэкенд локально

### Установите зависимости:

Убедитесь, что Python 3.11 установлен.

Установите PostgreSQL и создайте базу данных:

```
sudo apt install postgresql
psql -U postgres -c "CREATE DATABASE foodgram;"
```

### Склонируйте репозиторий:

```
git clone git@github.com:SharkFaceSF/foodgram.git
cd foodgram
```

### Создайте и активируйте виртуальное окружение:

```
python -m venv venv
source venv/bin/activate
```

### Установите зависимости:

```
pip install -r backend/requirements.txt
```

### Создайте файл .env:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Примените миграции и импортируйте ингредиенты:

```
cd backend
python manage.py migrate
python manage.py import_ingredients
```

### Создайте суперпользователя:

```
python manage.py createsuperuser
```

### Запустите сервер:

```
python manage.py runserver
```

API будет доступно по адресу `http://localhost:8000/api/`.

## Ссылка на развернутый проект

https://foodgramcoolproject.hopto.org/recipes

## Информация об авторе

- **Имя**: Максим
- **Email**: SharkFace34@yandex.ru
- **Username**: SharkFace34
- **Special features**: Всегда хочет спать, прямо сейчас особенно
