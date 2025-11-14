from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# For creating a new post
class PostCreate(BaseModel):
    title: str
    body: str
    
    @validator('title')
    def title_length(cls, v):
        if len(v) < 3:
            raise ValueError('Title must be at least 3 characters')
        if len(v) > 255:
            raise ValueError('Title must be less than 255 characters')
        return v
    
    @validator('body')
    def body_length(cls, v):
        if len(v) < 10:
            raise ValueError('Body must be at least 10 characters')
        return v

# For returning a post
class PostOut(BaseModel):
    id: int
    title: str
    body: str
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# External API post (from JSONPlaceholder)
class ExternalPost(BaseModel):
    userId: int
    id: int
    title: str
    body: str

# For listing external posts
class ExternalPostList(BaseModel):
    total: int
    page: int
    size: int
    posts: List[ExternalPost]