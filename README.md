# API Сервис:
1) Для получения списка товаров
2) Оформления заказов по полученному списку товаров
3) Принятие платежей по id заказа

Подвтерждение заказа происходит в админ-панели,
Обработку(изменение статуса и инициирование время подтверждения) выполняет celery-task.
После этого task отправляет POST-запрос по адресу https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4

Проект развернут на Django:

В качестве БД- PostgreSQL, как брокер-сообщений используется Redis и Сelery как планировщик задач.
Весь проект обернут в docker-compose



# Инструкция по установке проекта
1. Спулиться с ветки master:
2. Создать файл entrypoint.sh в директории app c содержимым:
__________________________________________________________________________________________
```
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py migrate

exec "$@"
```
_________________________________________________________________________________________
2.1. Если операционная система Mac или Linux прописать команду в терминале:
```
   chmod +x entrypoint.sh
```
__________________________________________________________________________________________


3. Запустить сборку контейнеров командой: ```docker-compose up -d --build```
4. <b>Эндпоинт получения списка Товаров</b> доступен GET-запросом по URL **http://127.0.0.1:8000/api/shop/products/**


<b>Пример Response-ответа</b>
~~~
   [
    {
        "id": 1,
        "name": "Apple",
        "text": "",
        "price": 5000,
        "image": null
    },
    {
        "id": 2,
        "name": "HP",
        "text": "",
        "price": 3000,
        "image": "http://127.0.0.1:8000/media/products_images/HP_7ez2bmQ.png"
    },
   ]
~~~

5. <b>Эндпоинт создания нового Заказа</b> доступен POST-запросом по URL **http://127.0.0.1:8000/api/shop/order/**

<b>Пример Json-тела:</b>
~~~
{
    "products": [1,2,4]
}
~~~
<b>Пример Response-овета:</b>

<b>Если указанные товары существуют:</b>
~~~
{
    "products": [
        1,
        3
    ]
}
~~~

<b>Если указанные товары не существуют:</b>
~~~
{
    "products": [
        "Недопустимый первичный ключ \"5\" - объект не существует."
    ]
}
~~~


6. <b>Эндпоинт создания нового Платежа</b> доступен POST-запросом по URL **http://127.0.0.1:8000/api/shop/payment/**

<b>Пример Json-тела:</b>
~~~
{
    "order": 1
}
~~~

<b>Пример Response-ответа:</b>

<b>Если платежа ещё не было:</b>
~~~
{
    "order": 1
}
~~~
<b>Если платеж уже существует по указанному заказу:</b>
~~~
{
    "order": [
        "Платеж с таким Заказ уже существует."
    ]
}
~~~
<b>Если указанный заказ не существует:</b>
~~~
{
    "order": [
        "Недопустимый первичный ключ \"4\" - объект не существует."
    ]
}
~~~

