from pydantic import BaseModel, EmailStr, constr
from typing import Annotated


class UserCreate(BaseModel):
    email: EmailStr
    username: Annotated[str,constr(min_length=3, max_length=20)]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str