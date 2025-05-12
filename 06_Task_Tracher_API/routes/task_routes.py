from fastapi import APIRouter, HTTPException
from models.task_models import TaskCreate, TaskUpdateStatus, Task
from storage import TASKS, USERS, task_id_counter

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    if task.user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    task_data = task.model_dump()
    task_data["id"] = task_id_counter
    TASKS[task_id_counter] = task_data
    task_id_counter += 1
    return task_data



@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.put("/{task_id}", response_model=Task)
def update_task_status(task_id: int, status_update: TaskUpdateStatus):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["status"] = status_update.status
    return task



@router.get("/user/{user_id}", response_model=list[Task])
def list_user_tasks(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return [task for task in TASKS.values() if task["user_id"] == user_id]