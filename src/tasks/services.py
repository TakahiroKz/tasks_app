from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, func
from math import ceil
from .models import Task
from src.tasks.dependencies import get_db
from src.tasks.models import Task as TaskModel
from src.tasks.schemas import Task_create, Task_response
from src.paginador.schemas import PaginatedResponse
from src.tasks.filters import build_task_filters

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: Task_create) -> Task_response:
        new_task = TaskModel(title=task.title,
                             description=task.description,
                             is_completed=task.is_completed)
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def get_task(self, task_id: int) ->Task_response:
        try:
            task = await self.db.get(TaskModel, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_tasks(self, page: int, limit: int, filters) -> PaginatedResponse[Task_response]:
        offset = (page - 1) * limit
        query_filters = build_task_filters(filters)
        try:
            count_query = (select(func.count()).select_from(TaskModel).where(*query_filters))
            total_res = await self.db.execute(count_query)
            total = total_res.scalar()
            pages = ceil(total/limit)
            query = (select(TaskModel).where(*query_filters).offset(offset).limit(limit))
            result = await self.db.execute(query)
            tasks = result.scalars().all()
            return PaginatedResponse[Task_response](
                items = tasks,
                total = total,
                page = page,
                limit = limit,
                pages = pages,
                has_next = page < pages,
                has_prev = page > 1
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def delete_task(self, task_id:int):
        try:
            task = await self.db.get(TaskModel, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            await self.db.delete(task)
            await self.db.commit()
            return {"message": "Task deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def update_task(self, task_id:int, task:Task_create) -> Task_response:
        try:
            existing_task = await self.db.get(TaskModel, task_id)
            if not existing_task:
                raise HTTPException(status_code=404, detail="Task not found")
            existing_task.title = task.title
            existing_task.description = task.description
            existing_task.is_completed = task.is_completed
            await self.db.commit()
            await self.db.refresh(existing_task)
            return existing_task
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

