Репозиторий для командного проекта Auth API.

## Запуск prod версии сервиса

`make prod-up` - запускает все сервисы.

После того, как все сервисы стартовали, API доступен по адресу http://127.0.0.1/api/
Спецификация http://127.0.0.1/api/openapi

## Запуск тестов в контейнере

`make tests-up`

## Локальный запуск сервиса

Для локального запуска необходимо в файл `.env.local` скопировать `.env`
и запустить `make local-up`.

Закомментировать `API_HOST`, `ES_HOST` и `REDIS_HOST` переменные в файле `.env`. 

Далее запустить `main.py`.

## Локальный запуск тестов

Для локального запуска тестов необходимо: 

- если это еще не сделано, поставить пакеты из `/auth-service/requirements.txt`

- содержимое .env.template копируем в .env в том же каталоге

- полученный файл .env копируем в папку /src/tests

- находясь в корне проекта, запустить `make tests-local-up`

- запустить локально приложение `main.py`

- из папки `/src/tests/functional/` запустить `pytest`


