from src.tasks.models import Task

TASK_FILTERS = {
    "title":lambda value: Task.title.ilike(f"%{value}%"),
    "completed": lambda value: Task.is_completed == value,
    "priority": lambda value: Task.priority == value
}