from fastapi import APIRouter, Depends, status, Query
from sqlalchemy import select

from .models import Task
from sqlalchemy.ext.asyncio import AsyncSession
from src.tasks.dependencies import get_db
from src.tasks.models import Task as TaskModel
from src.tasks.schemas import Task_create, Task_response
from src.tasks.services import TaskService
from src.paginador.core import pagination_params
from src.paginador.schemas import PaginatedResponse

tasks_router = APIRouter()

@tasks_router.post("/tasks", response_model=Task_response, status_code=status.HTTP_201_CREATED)
async def create_task(task:Task_create, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.create_task(task)

@tasks_router.get("/task/{task_id}", response_model=Task_response, status_code=status.HTTP_200_OK)
async def get_task(task_id: int, db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_task(task_id)

@tasks_router.get("/tasks", response_model=PaginatedResponse[Task_response], status_code=status.HTTP_200_OK)
async def get_tasks(db:AsyncSession = Depends(get_db), pagination = Depends(pagination_params)):
    service = TaskService(db)
    return await service.get_tasks(pagination["page"], pagination["limit"])

@tasks_router.delete("/task/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id:int, db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.delete_task(task_id)

@tasks_router.put("/task/{task_id}", response_model=Task_response, status_code=status.HTTP_200_OK)
async def update_task(task_id:int, task:Task_create, db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.update_task(task_id, task)

