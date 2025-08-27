# Используем официальный облегчённый образ Python
FROM python:3.10-slim

# Флаги для корректного вывода логов Python и запрета записи байт-кода
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновляем менеджер пакетов и устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями в контейнер
COPY pyproject.toml poetry.lock* /app/

# Обновляем pip и устанавливаем зависимости через Poetry без создания виртуального окружения
RUN pip install --upgrade pip setuptools wheel
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь проект в контейнер
COPY . /app/

# Применяем миграции и собираем статику при сборке (опционально)
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Открываем порт приложения
EXPOSE 8000

# Команда запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

