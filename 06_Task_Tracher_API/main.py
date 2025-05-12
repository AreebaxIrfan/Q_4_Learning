from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.task_routes import router as task_router

app = FastAPI(title="Task Tracker API")

@app.get("/")
def root():
    return {"message": "Task Tracker API is running!"}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])