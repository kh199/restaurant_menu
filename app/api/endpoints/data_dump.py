from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.report.create_data import CreateData, data_service
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
async def create_menus_for_report(service: CreateData = Depends(data_service)):
    """Наполнение базы готовыми данными
    для проверки функции генерирования отчета"""

    return await service.create_data_for_report()
