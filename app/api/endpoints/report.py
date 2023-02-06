import json
from datetime import datetime
from http import HTTPStatus

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import FORMAT
from app.core.db import get_async_session
from app.report.get_data import select_all_data
from app.report.tasks import write_report
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix="/report",
    tags=["Report"],
)


@router.post(
    "/",
    response_model=StatusMessage,
    status_code=HTTPStatus.ACCEPTED,
    summary="Запрос для генерации отчета",
)
async def create_task_for_report(
    session: AsyncSession = Depends(get_async_session),
) -> StatusMessage:
    menus = await select_all_data(session)
    menus = json.dumps(menus)
    task = write_report.apply_async(args=[menus])
    return StatusMessage(
        status=True,
        message=f"Task {task.id} has been created",
    )


@router.get(
    "/{task_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary="Запрос статуса и скачивание отчета",
)
async def get_task_status(
    task_id: str,
) -> StatusMessage | FileResponse:
    result = AsyncResult(task_id)
    if result.ready():
        return FileResponse(
            path=f"app/data/{task_id}.xlsx",
            media_type="application/octet-stream",
            filename=f"Меню от {datetime.now().strftime(FORMAT)}.xlsx",
        )
    return StatusMessage(
        status=True,
        message=f"Task {task_id} is {result.state}",
    )
