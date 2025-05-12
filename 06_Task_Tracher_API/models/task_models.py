from pydantic import BaseModel
from typing import Optional
from datetime import date
from utils.validators import validate_due_date, validate_status


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: str
    user_id: int

    _validate_due_date = validate_due_date
    _validate_status = validate_status


class TaskUpdateStatus(BaseModel):
    status: str
    _validate_status = validate_status


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: date
    status: str
    user_id: int

    _validate_due_date = validate_due_date
    _validate_status = validate_status