from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
from datetime import datetime, UTC
from uuid import uuid4
from typing import List, Optional
from fastapi.responses import JSONResponse

# Initialize FastAPI app with metadata
app = FastAPI(
    title="DACA Chatbot API",
    description="A modern API for a chatbot in the DACA tutorial series, built with FastAPI and Pydantic.",
    version="0.2.0",
    contact={
        "name": "DACA Tutorial Team",
        "url": "https://example.com",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# In-memory store for messages (for demonstration; use a database in production)
message_store: List[dict] = []

# Pydantic models
class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    session_id: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Serialize datetime to ISO format
        }

class Message(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)
    text: str = Field(..., min_length=1, max_length=1000)
    metadata: Metadata
    tags: Optional[List[str]] = None

    @validator("tags", each_item=True, pre=True)
    def validate_tags(cls, tag):
        if not tag.strip():
            raise ValueError("Tags cannot be empty strings")
        return tag.strip()

class Response(BaseModel):
    user_id: str
    reply: str
    metadata: Metadata
    status: str = "success"

# Root endpoint
@app.get("/", summary="Welcome message")
async def root():
    return {"message": "Welcome to the DACA Chatbot API v0.2.0! Explore /docs for interactive API documentation."}

# GET endpoint to retrieve user info
@app.get(
    "/users/{user_id}",
    summary="Get user information",
    response_model=dict,
    responses={
        200: {"description": "User info retrieved successfully"},
        400: {"description": "Invalid user ID"}
    }
)
async def get_user(user_id: str, role: Optional[str] = None):
    if not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID cannot be empty")
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

# POST endpoint for chatting
@app.post(
    "/chat/",
    summary="Send a chat message",
    response_model=Response,
    responses={
        200: {"description": "Message processed successfully"},
        400: {"description": "Invalid message input"}
    }
)
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    
    # Store message (for demonstration)
    message_store.append(message.dict())
    
    reply_text = f"Hello, {message.user_id}! You said: '{message.text}'. How can I assist you today?"
    response = Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata(),
        status="success"
    )
    return response

# GET endpoint to list recent messages
@app.get(
    "/messages/",
    summary="List recent messages",
    response_model=List[Message],
    responses={
        200: {"description": "List of recent messages"},
        404: {"description": "No messages found"}
    }
)
async def get_messages(limit: int = 10):
    if not message_store:
        raise HTTPException(status_code=404, detail="No messages found")
    return message_store[-limit:]

# Exception handler for generic errors
@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )