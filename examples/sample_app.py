"""
Example FastAPI Application

This is a sample FastAPI application to demonstrate the AutoDocGen system.
"""

from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime

# Create FastAPI app with metadata
app = FastAPI(
    title="Sample API",
    description="A sample FastAPI application for AutoDocGen demonstration",
    version="1.0.0"
)

# Enums
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

# Pydantic Models
class User(BaseModel):
    """User model representing a user in the system"""
    id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    email: str = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    status: UserStatus = Field(UserStatus.ACTIVE, description="User's current status")
    created_at: datetime = Field(default_factory=datetime.now, description="User creation timestamp")

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="User's email address")
    full_name: Optional[str] = None

# In-memory storage (for demo purposes)
users_db: Dict[str, User] = {}

# Root endpoint
@app.get("/", tags=["General"])
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Welcome to the Sample API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# Health check endpoint
@app.get("/health", tags=["General"], summary="Health Check")
async def health_check():
    """Check the health status of the API"""
    return {"status": "healthy", "timestamp": datetime.now()}

# User endpoints
@app.post("/users", tags=["Users"], summary="Create User")
async def create_user(user: UserCreate = Body(..., description="User data")):
    """Create a new user in the system"""
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name
    )
    users_db[user_id] = new_user
    
    return {
        "success": True,
        "message": "User created successfully",
        "data": new_user.dict()
    }

@app.get("/users", tags=["Users"], summary="List Users")
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return")
):
    """Get a list of users with optional filtering"""
    users = list(users_db.values())[skip:skip + limit]
    
    return {
        "success": True,
        "message": f"Retrieved {len(users)} users",
        "data": [user.dict() for user in users]
    }

@app.get("/users/{user_id}", tags=["Users"], summary="Get User")
async def get_user(
    user_id: str = Path(..., description="User ID to retrieve")
):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "message": "User retrieved successfully",
        "data": users_db[user_id].dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
