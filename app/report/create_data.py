import json

import aiofiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.dish import dish_crud
from app.crud.menu import menu_crud
from app.crud.submenu import submenu_crud
from app.schemas.status import StatusMessage


async def load_data_for_report():
    async with aiofiles.open("app/report/report_data.json", mode="r") as f:
        data = await f.read()

    menus = json.loads(data)
    return menus


class CreateData:
    def __init__(self, session):
        self.session = session

    async def create_data_for_report(self):
        menus = await load_data_for_report()
        for menu in menus:
            await menu_crud.create_from_dict(
                id=menu["id"],
                title=menu["title"],
                description=menu["description"],
                session=self.session,
            )

            for submenu in menu["submenus"]:
                await submenu_crud.create_submenu_from_dict(
                    id=submenu["id"],
                    title=submenu["title"],
                    description=submenu["description"],
                    parent_id=submenu["menu_id"],
                    session=self.session,
                )

                for dish in submenu["dishes"]:
                    await dish_crud.create_dish_from_dict(
                        id=dish["id"],
                        title=dish["title"],
                        description=dish["description"],
                        price=dish["price"],
                        parent_id=dish["submenu_id"],
                        session=self.session,
                    )

        return StatusMessage(
            status=True,
            message="Data has been created",
        )


async def data_service(session: AsyncSession = Depends(get_async_session)):
    return CreateData(session=session)
