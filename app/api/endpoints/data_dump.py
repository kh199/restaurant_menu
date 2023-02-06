from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.report.create_data import create_data_for_report
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix="/dump",
    tags=["Data Dump"],
)


@router.post(
    "/",
    response_model=StatusMessage,
    status_code=HTTPStatus.CREATED,
    summary="Наполнение базы данных",
)
async def create_menus_for_report(
    session: AsyncSession = Depends(get_async_session),
) -> StatusMessage:
    """Наполнение базы готовыми данными
    для проверки функции генерирования отчета"""

    return await create_data_for_report(session)
