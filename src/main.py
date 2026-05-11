from fastapi import FastAPI
from .tasks.router import tasks_router

app = FastAPI()
app.include_router(tasks_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"Message":"task-app is up"}
