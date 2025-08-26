## Описание:

Учебный проект

## Как запустить проект:

Команды нужно выполнять из папки с проектом.

1. Клонируйте репозиторий:
```
    git clone https://github.com/masadara/djangoREST
```
2. Установите зависимости:
```
    poetry install
```
3. Создайте и заполните данными файл <b>.env</b> по примеру <b>.env.sample</b>

4. Примените миграции

```
    python manage.py migrate
```

5. Запустите проект командой:

```
    docker-compose up --build
```

6. Проверьте доступность базы:

```
    docker-compose exec web python manage.py dbshell
```

7. Перейти по адресу: http://127.0.0.1:8000

