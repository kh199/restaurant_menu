import xlsxwriter
from datetime import datetime
import json

FORMAT = "%d.%m.%Y"


def load_data_for_report():
    with open('app/report/report_data.json', mode='r', encoding='utf-8') as f:
        data = f.read()

    menus = json.loads(data)
    return menus


menus = load_data_for_report()

now_date_time = datetime.now().strftime(FORMAT)
workbook = xlsxwriter.Workbook(f'app/report/Меню от {now_date_time}.xlsx')
worksheet = workbook.add_worksheet()

set_format = workbook.add_format()
set_format.set_bold()
set_format.set_font_size(12)

menu_row = 0
menu_count = 1
menu_gap = 1

submenu_count = 1
submenu_row = 1

dish_count = 1
dish_row = 2

for menu in menus:

    worksheet.write(menu_row, 0, menu_count, set_format)
    worksheet.write(menu_row, 1, menu['title'], set_format)
    worksheet.write(menu_row, 2, menu['description'], set_format)
    menu_count += 1

    for submenu in menu['submenus']:
        worksheet.write(submenu_row, 1, submenu_count, set_format)
        worksheet.write(submenu_row, 2, submenu['title'], set_format)
        worksheet.write(submenu_row, 3, submenu['description'], set_format)
        submenu_row += len(submenu['dishes']) + 1
        submenu_count += 1
        menu_gap += len(submenu['dishes'])

        for dish in submenu['dishes']:
            worksheet.write(dish_row, 2, dish_count, set_format)
            worksheet.write(dish_row, 3, dish['title'], set_format)
            worksheet.write(dish_row, 4, dish['description'], set_format)
            worksheet.write(dish_row, 5, dish['price'], set_format)
            dish_row += 1
            dish_count += 1
        dish_count = 1
        dish_row += 1

    menu_row += len(menu['submenus']) + menu_gap
    submenu_row += 1
    dish_row += 1
    submenu_count = 1
    dish_count = 1


workbook.close()
