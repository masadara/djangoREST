# Используем официальный Python базовый образ
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию приложения в контейнере
WORKDIR /app

# Копируем файлы для установки зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем зависимости проекта через Poetry в виртуальное окружение
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Копируем исходники проекта
COPY . /app/

# Выполняем миграции и собираем статику при билде (опционально)
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Открываем порт приложения
EXPOSE 8000

# Команда запуска проекта через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
