import json
import os
from datetime import datetime
from http import HTTPStatus

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
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
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary="Запрос статуса",
)
async def get_task_status(
    task_id: str,
) -> FileResponse | dict:
    result = AsyncResult(task_id)
    if result.successful():
        return StatusMessage(
            status=True,
            message="Task is ready",
        )
    raise HTTPException(status_code=425, detail="Task is not ready or not found")


@router.get(
    "/{task_id}/download",
    response_class=FileResponse,
    status_code=HTTPStatus.OK,
    summary="Загрузка готового отчета",
)
async def get_report(
    task_id: str,
) -> FileResponse:
    data_path = f"app/data/{task_id}.xlsx"
    if os.path.exists(data_path):
        filename = f"Menu {datetime.now().strftime(FORMAT)}.xlsx"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        return FileResponse(
            path=data_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
            headers=headers,
        )
    raise HTTPException(status_code=404, detail="Report not found")
