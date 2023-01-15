from fastapi import APIRouter

from app.api.endpoints import dish_router, menu_router, submenu_router

main_router = APIRouter(prefix='/api/v1/menus')
main_router.include_router(menu_router)
main_router.include_router(submenu_router,
                           prefix='/{menu_id}/submenus')
main_router.include_router(dish_router,
                           prefix='/{menu_id}/submenus/{submenu_id}/dishes')
