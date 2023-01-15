# REST API для меню ресторана
---

#### Метод    |       #### Эндпоинт  | #### Функция
-----------|------------------------|------------------
**POST**  |   ```/api/v1/menus```   |создание меню
**GET**   |   ```/api/v1/menus```   | просмотр списка меню
**PATCH**  |  ```/api/v1/menus/{menu_id}``` | обновление меню
**GET**    |  ```/api/v1/menus/{menu_id}``` |просмотр определенного меню
**DELETE**  | ```/api/v1/menus/{menu_id}``` |удаление меню

**POST**   |  ```/api/v1/menus/{menu_id}/submenus/```| создание подменю
**GET**    |  ```/api/v1/menus/{menu_id}/submenus/``` |просмотр списка подменю
**PATCH**  |  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` |обновление подменю
**GET**    |  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` |просмотр определенного подменю
**DELETE** |  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}``` |удаление подменю

**POST**   |  ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` |создание блюда
**GET**     | ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes``` |просмотр списка блюд
**PATCH**   | ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` |обновление блюда
**GET**     | ```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` |просмотр определенного блюда
**DELETE**   |```/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}``` |удаление блюда

---
### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/kh199/restaurant_menu
```

Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Запустить приложение:
```
uvicorn app.main:app
```

---
# Стек
+ Python 11
+ FastAPI
+ SQLite


# Автор
**Екатерина Каричева** [kh199](https://github.com/kh199)