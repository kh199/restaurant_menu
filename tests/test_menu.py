import json

from httpx import AsyncClient

from tests.test_data import menu_data, menu_keys, updated_menu_data


async def test_get_empty_menu_list(async_client: AsyncClient):
    """Запрос к пустой датабазе"""

    response = await async_client.get("/api/v1/menus/")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data == []


async def test_create_menu(async_client: AsyncClient):
    """Создание меню"""

    response = await async_client.post(
        "/api/v1/menus/",
        data=json.dumps(menu_data),
    )
    resp_data = response.json()
    assert (
        sorted(list(resp_data.keys())) == menu_keys
    ), f"При POST-запросе к `/api/v1/menus/` в ответе нет `{menu_keys}`."
    assert response.status_code == 201
    assert resp_data["title"] == menu_data["title"]
    assert resp_data["description"] == menu_data["description"]
    assert resp_data["submenus_count"] == 0
    assert resp_data["dishes_count"] == 0


async def test_get_menu_list(async_client: AsyncClient, create_menu):
    """Просмотр списка меню"""

    response = await async_client.get("/api/v1/menus/")
    assert response.status_code == 200
    resp_data = response.json()
    assert isinstance(resp_data, list)
    assert len(resp_data) == 1


async def test_get_menu_by_id(async_client: AsyncClient, create_menu):
    """Просмотр меню по id"""

    id_response = await async_client.get(f"/api/v1/menus/{create_menu.id}")
    id_resp_data = id_response.json()
    assert id_response.status_code == 200
    assert sorted(list(id_resp_data.keys())) == menu_keys
    assert id_resp_data["title"] == menu_data["title"]
    assert id_resp_data["description"] == menu_data["description"]
    assert id_resp_data["submenus_count"] == 0
    assert id_resp_data["dishes_count"] == 0


async def test_get_menu_not_found(async_client: AsyncClient):
    """GET-запрос к несуществующему меню"""

    menu_id = "not-id"
    response = await async_client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data["detail"] == "menu not found"


async def test_update_menu(async_client: AsyncClient, create_menu):
    """Обновление меню"""

    patch_resp = await async_client.patch(
        f"/api/v1/menus/{create_menu.id}",
        data=json.dumps(updated_menu_data),
    )
    patch_data = patch_resp.json()
    assert patch_resp.status_code == 200
    assert sorted(list(patch_data.keys())) == menu_keys
    assert patch_data["title"] == updated_menu_data["title"]
    assert patch_data["description"] == updated_menu_data["description"]
    assert patch_data["submenus_count"] == 0
    assert patch_data["dishes_count"] == 0


async def test_patch_menu_not_found(async_client: AsyncClient):
    """PATCH-запрос к несуществующему меню"""

    menu_id = "not-id"
    response = await async_client.patch(
        f"/api/v1/menus/{menu_id}",
        data=json.dumps(updated_menu_data),
    )
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data["detail"] == "menu not found"


async def test_delete_menu(async_client: AsyncClient, create_menu):
    """Удаление меню"""

    delete_resp = await async_client.delete(f"/api/v1/menus/{create_menu.id}")
    delete_data = delete_resp.json()
    assert delete_resp.status_code == 200
    assert delete_data["status"] is True
    assert delete_data["message"] == "The menu has been deleted"
    deleted_resp = await async_client.get(f"/api/v1/menus/{create_menu.id}")
    assert deleted_resp.status_code == 404
