from fastapi import FastAPI
from .tasks.router import tasks_router
from .auth.router import login_router

app = FastAPI()
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(login_router, prefix="/auth")

@app.get("/")
def root():
    return {"Message":"task-app is up"}
