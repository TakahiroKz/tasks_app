from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User

from .models import Task
from src.tasks.dependencies import get_db
from src.tasks.models import Task as TaskModel
from src.tasks.schemas import Task_create, Task_response, TaskFilterParams
from src.tasks.services import TaskService
from src.paginador.core import pagination_params
from src.paginador.schemas import PaginatedResponse
from src.auth.dependencies import get_current_user


tasks_router = APIRouter()

@tasks_router.post("/tasks", response_model=Task_response, status_code=status.HTTP_201_CREATED)
async def create_task(task:Task_create,current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.create_task(task,current_user)

@tasks_router.get("/task/{task_id}", response_model=Task_response, status_code=status.HTTP_200_OK)
async def get_task(task_id: int, current_user: User = Depends(get_current_user) ,db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_task(task_id,current_user)

@tasks_router.get("/tasks", response_model=PaginatedResponse[Task_response], status_code=status.HTTP_200_OK)
async def get_tasks(current_user = Depends(get_current_user),sort_by:str="created_at", order:str = "desc", filters: TaskFilterParams = Depends(), pagination = Depends(pagination_params),db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_tasks(current_user,pagination["page"], pagination["limit"], filters, sort_by, order)

@tasks_router.delete("/task/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id:int, current_user: User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.delete_task(task_id)

@tasks_router.put("/task/{task_id}", response_model=Task_response, status_code=status.HTTP_200_OK)
async def update_task(task_id:int, task:Task_create, current_user: User = Depends(get_current_user), db:AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.update_task(task_id, task)

