from src.tasks.models import Task

def build_task_filters(filters):
    query_filters = []
    if filters.title:
        query_filters.append(
            Task.title.ilike(f"%{filters.title}%")
        )
    if filters.completed is not None:
        query_filters.append(
            Task.is_completed == filters.completed
        )
    if filters.priority is not None:
        query_filters.append(
            Task.priority == filters.priority
        )
    return query_filters