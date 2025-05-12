from fastapi import APIRouter, HTTPException
from models.user_models import UserCreate, UserRead
from storage import USERS, user_id_counter

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate):
    global user_id_counter
    user_data = user.model_dump()
    user_data["id"] = user_id_counter
    USERS[user_id_counter] = user_data
    user_id_counter += 1
    return user_data



@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user