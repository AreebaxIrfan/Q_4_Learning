from datetime import date
from pydantic import validator

@validator("due_date")
def validate_due_date(cls, value):
    if value < date.today():
        raise ValueError("Due date must be today or in the future.")
    return value

@validator("status")
def validate_status(cls, value):
    allowed = ["pending", "in-progress", "completed"]
    if value not in allowed:
        raise ValueError(f"Status must be one of {allowed}")
    return value