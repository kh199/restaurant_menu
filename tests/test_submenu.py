import json

from httpx import AsyncClient

from tests.test_data import (
    submenu_data,
    submenu_keys,
    updated_menu_data,
    updated_submenu_data,
)


async def test_create_submenu(async_client: AsyncClient, create_menu):
    """Создание подменю"""

    response = await async_client.post(
        f"/api/v1/menus/{create_menu.id}/submenus/",
        data=json.dumps(submenu_data),
    )
    resp_data = response.json()
    assert response.status_code == 201
    assert sorted(list(resp_data.keys())) == submenu_keys
    assert resp_data["title"] == submenu_data["title"]
    assert resp_data["description"] == submenu_data["description"]
    assert resp_data["dishes_count"] == 0


async def test_get_submenu_list(async_client: AsyncClient, create_submenu):
    """Просмотр списка подменю"""

    menu_id = create_submenu.parent_id
    response = await async_client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    subresp_data = response.json()
    assert isinstance(subresp_data, list)
    assert len(subresp_data) == 1


async def test_get_empty_submenu_list(async_client: AsyncClient, create_menu):
    """Просмотр пустого списка подменю"""

    response = await async_client.get(
        f"/api/v1/menus/{create_menu.id}/submenus/",
    )
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data == []


async def test_get_submenu_by_id(async_client: AsyncClient, create_submenu):
    """Просмотр подменю по id"""

    menu_id = create_submenu.parent_id
    response = await async_client.get(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}",
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert sorted(list(resp_data.keys())) == submenu_keys
    assert resp_data["title"] == submenu_data["title"]
    assert resp_data["description"] == submenu_data["description"]
    assert resp_data["dishes_count"] == 0


async def test_get_submenu_not_found(async_client: AsyncClient, create_menu):
    """GET-запрос к несуществующему подменю"""

    submenu_id = "not-id"
    response = await async_client.get(
        f"/api/v1/menus/{create_menu.id}/submenus/{submenu_id}",
    )
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data["detail"] == "submenu not found"


async def test_update_submenu(async_client: AsyncClient, create_submenu):
    """Обновление подменю"""

    menu_id = create_submenu.parent_id
    response = await async_client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}",
        data=json.dumps(updated_submenu_data),
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert sorted(list(resp_data.keys())) == submenu_keys
    assert resp_data["title"] == updated_submenu_data["title"]
    assert resp_data["description"] == updated_submenu_data["description"]
    assert resp_data["dishes_count"] == 0


async def test_patch_submenu_not_found(async_client: AsyncClient, create_menu):
    """PATCH-запрос к несуществующему подменю"""

    submenu_id = "not-id"
    response = await async_client.patch(
        f"/api/v1/menus/{create_menu.id}/submenus/{submenu_id}",
        data=json.dumps(updated_menu_data),
    )
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data["detail"] == "submenu not found"


async def test_delete_submenu(async_client: AsyncClient, create_submenu):
    """Удаление подменю"""

    menu_id = create_submenu.parent_id
    response = await async_client.delete(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}",
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data["status"] is True
    assert resp_data["message"] == "The submenu has been deleted"
    deleted_resp = await async_client.get(
        f"/api/v1/menus/{menu_id}/submenus/{create_submenu.id}",
    )
    assert deleted_resp.status_code == 404
