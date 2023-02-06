menu_data = {
    "title": "My menu 1",
    "description": "My menu description 1",
}

updated_menu_data = {
    "title": "My updated menu 1",
    "description": "My updated menu description 1",
}

submenu_data = {
    "title": "My submenu 1",
    "description": "My submenu description 1",
}

updated_submenu_data = {
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1",
}

dish_data = {
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50",
}

updated_dish_data = {
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50",
}

menu_keys = sorted(
    [
        "id",
        "title",
        "description",
        "submenus_count",
        "dishes_count",
    ],
)

submenu_keys = sorted(
    [
        "id",
        "title",
        "description",
        "dishes_count",
    ],
)

dish_keys = sorted(
    [
        "id",
        "title",
        "description",
        "price",
    ],
)
