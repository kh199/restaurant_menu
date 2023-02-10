# REST API для меню ресторана

Стек:

```FastAPI```
```PostgreSQL```
```Docker```
```Pytest```
```Redis```
```Celery```
```RabbitMQ```

Асинхронное приложение по работе с меню ресторана. Реализованы 3 сущности: Меню, Подменю, Блюдо.
Зависимости:
+ У меню есть подменю
+ В подменю есть блюда

Реализовано кэширование, в качестве кэш-хранилища используется Redis.

В проекте есть фоновая задача для выгрузки меню в виде excel-документа, реализованная с помощью Celery + RabbitMQ.

#### Запустить приложение
```
docker-compose up -d
```
#### Запустить тесты
```
docker-compose -f docker-compose.tests.yml up
```
Документация доступна по адресу ```http://127.0.0.1:8000/docs```

### Data Dump
+ **POST**   ```/api/v1/dump``` наполнение базы готовыми данными

### Report
+ **POST**   ```/api/v1/report``` запрос для генерации отчета в формате xlsx
+ **GET**   ```/api/v1/report/{task_id}``` запрос статуса задачи
+ **GET**   ```/api/v1/report/{task_id}/download``` скачивание отчета

### Menus
+ **POST**   ```/api/v1/menus```создание меню
+ **GET** ```/api/v1/menus``` просмотр списка меню
+ **PATCH** ```/api/v1/menus/{menu_id}``` обновление меню
+ **GET**    ```/api/v1/menus/{menu_id}```просмотр определенного меню
+ **DELETE**  ```/api/v1/menus/{menu_id}``` удаление меню

### Submenus
+ **POST** ```/api/v1/menus/{menu_id}/submenus/``` создание подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/``` просмотр списка подменю
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` обновление подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` просмотр определенного подменю
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` удаление подменю

### Dishes
+ **POST** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` создание блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` просмотр списка блюд
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` обновление блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` просмотр определенного блюда
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` удаление блюда
