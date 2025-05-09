# DACA Chatbot API

A modern, FastAPI-based API for a chatbot in the DACA tutorial series, built with FastAPI and Pydantic. This API supports user interactions, message storage, and provides interactive documentation via Swagger UI.

## Features
- **Root Endpoint**: `GET /` - Welcome message.
- **User Info**: `GET /users/{user_id}` - Retrieve user information with an optional role query parameter.
- **Chat Endpoint**: `POST /chat/` - Send and receive chat messages with Pydantic validation.
- **Message History**: `GET /messages/` - Retrieve recent messages (in-memory for demo).
- **Enhanced Validation**: Robust input validation using Pydantic models.
- **Interactive Docs**: Access Swagger UI at `/docs` for testing endpoints.

## Prerequisites
- **Python**: 3.13.3 (or 3.12.x for compatibility).
- **uv**: Package and virtual environment manager (install via `pip install uv`).
- **Windows**: Commands are for Windows Command Prompt (CMD). For MINGW64, adjust activation syntax.

## Setup Instructions
1. **Clone or Navigate to Project Directory**:
   ```cmd
   cd D:\a-works\Q4_learning\03_Pydantic\pydantic_project