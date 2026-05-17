from src.tasks.models import Task as TaskModel

TASK_SORT_FIELDS = {
    "title": TaskModel.title,
    "created_at": TaskModel.created_at,
    "priority": TaskModel.priority
}