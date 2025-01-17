# Dogs API - DRF + PostgreSQL

## URLs:

- GET /dogs/ - получение списка всех сохраненных собак
- POST /dogs/ - создание новой собаки
- PUT, DELETE /dogs/\<id>/ - модификация, удаление собаки по id
- GET /breeds/ - получение списка всех сохраненных пород собак
- POST /breeds/ - создание новой породы
- PUT, DELETE /breeds/\<id>/ - модификация, удаление породы по id
- /admin/ - админ панель
## Models:

Модель Dog
- name (строка символов)
- age (целое число)
- breed (внешний ключ к модели Breed)
- gender (строка символов)
- color (строка символов)
- favorite_food (строка символов)
- favorite_toy (строка символов)


Модель Breed
- Порода должна содержать следующие поля:
- name (строка символов)
- size (строка символов) [Tiny, Small, Medium, Large]
- friendliness (поле целого числа) [от 1 до 5]
- trainability (поле целого числа) [от 1 до 5]
- shedding_amount (поле целого числа) [от 1 до 5]
- exercise_needs (поле целого числа) [от 1 до 5]

## Примеры запросов:

- Пример ответа GET /dogs/
```json
[
  {
    "id": 2,
    "avg_breed_age": "1.00",
    "name": "Жучка",
    "age": 1,
    "gender": "Female",
    "color": "Белый",
    "favorite_food": "Цыпленок",
    "favorite_toy": "Мяч",
    "breed": 1
  },
  ...
]
```
Поле avg_breed_age вычисляется "на лету" Postgre, показывает средний возраст собак этой породы
- Пример ответа GET /dogs/\<id>
```json
{
  "id": 1,
  "same_breed_count": 1,
  "name": "Барбос",
  ...
  "breed": 2
}
```
Поле same_breed_count вычисляется "на лету" Postgre, показывает количество пород той же породы
- Пример ответа GET /breeds/
```json
[
  {
    "id": 1,
    "dogs_count": 1,
    "name": "Такса",
    "size": "Small",
    "friendliness": 5,
    "trainability": 3,
    "shedding_amount": 1,
    "exercise_needs": 1
  },
  ...
]
```
Поле dogs_count вычисляется "на лету" Postgre, показывает количество пород той же породы
- Пример body для POST /dogs/
```json
{
    "name": "Жучка",
    "age": 1,
    "gender": "Female",
    "color": "Белый",
    "favorite_food": "Цыпленок",
    "favorite_toy": "Мяч",
    "breed": 1
}
```
- Пример body для POST /breeds/
```json
{
    "name": "Такса",
    "size": "Small",
    "friendliness": 5,
    "trainability": 3,
    "shedding_amount": 1,
    "exercise_needs": 1
}
```

## Usage
local:
- python3 -m venv venv
- pip install poetry
- poetry install
- создать файл .env по аналогии с .env.example
- ./manage.py migrate
- ./manage.py createsuperuser (создайте администратора)
- ./manage.py runserver


Docker:
- задайте .env-non-dev
- docker-compose build
- docker-compose up
- docker-compose run --rm web-app sh -c "./manage.py migrate"
- docker-compose run --rm web-app sh -c "./manage.py createsuperuser"
- docker-compose run --rm web-app sh -c "./manage.py runserver 0.0.0.0:8000"

