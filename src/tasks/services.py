from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, func, asc, desc
from math import ceil

from .models import Task
from src.tasks.dependencies import get_db
from src.tasks.models import Task as TaskModel
from src.tasks.schemas import Task_create, Task_response
from src.paginador.schemas import PaginatedResponse
from src.tasks.filters import TASK_FILTERS
from src.tasks.sort import TASK_SORT_FIELDS

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: Task_create,current_user) -> Task_response:
        new_task = TaskModel(title=task.title,
                             description=task.description,
                             is_completed=task.is_completed,
                             priority=task.priority,
                             user_id=current_user.id)
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def get_task(self, task_id: int, current_user) ->Task_response:
        try:
            task = await self.db.get(TaskModel, task_id)
            if not task or task.user_id != current_user.id:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_tasks(self, current_user,page: int, limit: int, filters: dict, sort_by:str = "created_at", order:str="desc") -> PaginatedResponse[Task_response]:
        offset = (page - 1) * limit
        filters = dict(filters)
        try:
            count_query = (select(func.count()).select_from(TaskModel))
            for field, value in filters.items():
                if value is None:
                    continue    
                filter_func = TASK_FILTERS.get(field)
                if filter_func:
                    count_query = count_query.where(filter_func(value))
            count_query = count_query.where(TaskModel.user_id == current_user.id)
            total_res = await self.db.execute(count_query)
            total = total_res.scalar()
            pages = ceil(total/limit)
            query = (select(TaskModel).offset(offset).limit(limit))
            for field, value in filters.items():
                if value is None:
                    continue
                filter_func = TASK_FILTERS.get(field)
                if filter_func:
                    query = query.where(filter_func(value))
            
            sort_column = TASK_SORT_FIELDS.get(sort_by)
            if sort_column:
                if order == "asc":
                    query = query.order_by(asc(sort_column))
                else:
                    query = query.order_by(desc(sort_column))
            query = query.where(TaskModel.user_id == current_user.id)
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
            existing_task.pririty = task.priority
            await self.db.commit()
            await self.db.refresh(existing_task)
            return existing_task
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

