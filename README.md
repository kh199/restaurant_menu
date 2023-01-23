# REST API для меню ресторана


#### Запустить приложение
```
docker-compose up -d --build
```

#### Запустить тесты
```
docker-compose -f docker-compose.tests.yml up --build
```

Документация доступна по адресу ```http://127.0.0.1:8000/docs```


### Меню
+ **POST**   ```/api/v1/menus```создание меню
+ **GET** ```/api/v1/menus``` просмотр списка меню
+ **PATCH** ```/api/v1/menus/{menu_id}``` обновление меню
+ **GET**    ```/api/v1/menus/{menu_id}```просмотр определенного меню
+ **DELETE**  ```/api/v1/menus/{menu_id}``` удаление меню

### Подменю
+ **POST** ```/api/v1/menus/{menu_id}/submenus/``` создание подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/``` просмотр списка подменю
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` обновление подменю
+ **GET**  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` просмотр определенного подменю
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` удаление подменю

### Блюда
+ **POST** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` создание блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` просмотр списка блюд
+ **PATCH** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` обновление блюда
+ **GET**   ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` просмотр определенного блюда
+ **DELETE** ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` удаление блюда
