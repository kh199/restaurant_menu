import json
from datetime import datetime
from http import HTTPStatus

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.cache.services.menu_service import MenuCache, menu_service
from app.core.config import FORMAT
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
    service: MenuCache = Depends(menu_service),
) -> StatusMessage:
    menus = await service.get_all_data()
    menus = json.dumps(menus)
    task = write_report.apply_async(args=[menus])
    return StatusMessage(
        status=True,
        message=f"Task {task.id} has been created",
    )


@router.get(
    "/{task_id}",
    response_class=FileResponse,
    response_model=None,
    status_code=HTTPStatus.OK,
    summary="Запрос статуса и скачивание отчета",
)
async def get_task_status(
    task_id: str,
) -> FileResponse | dict:
    result = AsyncResult(task_id)
    if result.ready():
        filename = f"Menu {datetime.now().strftime(FORMAT)}.xlsx"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        return FileResponse(
            path=f"app/data/{task_id}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
            headers=headers,
        )
    return {"message": f"Task {task_id} is {result.state}"}
