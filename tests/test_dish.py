import json

from httpx import AsyncClient

from app.models import Menu, SubMenu
from tests.conftest import db
from tests.test_data import dish_data, dish_keys, updated_dish_data


async def test_create_dish(async_client: AsyncClient, create_submenu):
    """Создание блюда"""

    menu_id = create_submenu.parent_id
    response = await async_client.post(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}/dishes/",
        data=json.dumps(dish_data),
    )
    resp_data = response.json()
    assert response.status_code == 201
    assert sorted(list(resp_data.keys())) == dish_keys
    assert resp_data["title"] == dish_data["title"]
    assert resp_data["description"] == dish_data["description"]
    assert resp_data["price"] == dish_data["price"]


async def test_get_dish_list(async_client: AsyncClient, create_dish):
    """Просмотр списка блюд"""

    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(parent_id=menu.id).first()
    response = await async_client.get(
        f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/",
    )
    assert response.status_code == 200
    resp_data = response.json()
    assert isinstance(resp_data, list)
    assert len(resp_data) == 1


async def test_get_empty_dish_list(async_client: AsyncClient, create_submenu):
    """Просмотр пустого списка блюд"""

    menu_id = create_submenu.parent_id
    response = await async_client.get(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}/dishes/",
    )
    assert response.status_code == 200
    subresp_data = response.json()
    assert subresp_data == []


async def test_get_dish_by_id(async_client: AsyncClient, create_dish):
    """Просмотр блюда по id"""

    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(parent_id=menu.id).first()
    response = await async_client.get(
        f"/api/v1/menus/{menu.id}/submenus/" f"{submenu.id}/dishes/{create_dish.id}",
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert sorted(list(resp_data.keys())) == dish_keys
    assert resp_data["title"] == dish_data["title"]
    assert resp_data["description"] == dish_data["description"]
    assert resp_data["price"] == dish_data["price"]


async def test_get_dish_not_found(
    async_client: AsyncClient,
    create_submenu,
):
    """GET-запрос к несуществующему блюду"""

    menu_id = create_submenu.parent_id
    dish_id = "not-id"
    subresp = await async_client.get(
        f"/api/v1/menus/{menu_id}/submenus/" f"{create_submenu.id}/dishes/{dish_id}",
    )
    assert subresp.status_code == 404
    resp_data = subresp.json()
    assert resp_data["detail"] == "dish not found"


async def test_update_dish(async_client: AsyncClient, create_dish):
    """Обновление блюда"""

    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(parent_id=menu.id).first()
    response = await async_client.patch(
        f"/api/v1/menus/{menu.id}/submenus/" f"{submenu.id}/dishes/{create_dish.id}",
        data=json.dumps(updated_dish_data),
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert sorted(list(resp_data.keys())) == dish_keys
    assert resp_data["title"] == updated_dish_data["title"]
    assert resp_data["description"] == updated_dish_data["description"]
    assert resp_data["price"] == updated_dish_data["price"]


async def test_patch_dish_not_found(
    async_client: AsyncClient,
    create_submenu,
):
    """PATCH-запрос к несуществующему блюду"""

    menu_id = create_submenu.parent_id
    dish_id = "not-id"
    response = await async_client.patch(
        f"/api/v1/menus/{menu_id}/submenus/" f"{create_submenu.id}/dishes/{dish_id}",
        data=json.dumps(updated_dish_data),
    )
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data["detail"] == "dish not found"


async def test_delete_dish(async_client: AsyncClient, create_dish):
    """Удаление блюда"""

    menu = db.query(Menu).first()
    submenu = db.query(SubMenu).filter_by(parent_id=menu.id).first()
    response = await async_client.delete(
        f"/api/v1/menus/{menu.id}/submenus/" f"{submenu.id}/dishes/{create_dish.id}",
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data["status"] is True
    assert resp_data["message"] == "The dish has been deleted"
    deleted_resp = await async_client.get(
        f"/api/v1/menus/{menu.id}/submenus/" f"{submenu.id}/dishes/{create_dish.id}",
    )
    assert deleted_resp.status_code == 404
