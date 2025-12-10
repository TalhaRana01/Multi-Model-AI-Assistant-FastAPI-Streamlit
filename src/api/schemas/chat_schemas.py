"""
Pydantic schemas for chat/LLM interactions
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Schema for chat request"""
    message: str = Field(..., min_length=1, max_length=10000)
    provider: Optional[str] = Field("openai", description="LLM provider (openai/anthropic)")
    model: Optional[str] = Field(None, description="Model name")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000)


class ChatResponse(BaseModel):
    """Schema for chat response"""
    response: str
    provider: str
    model: str
    tokens_used: int
    cost: float
    timestamp: datetime


class ConversationHistory(BaseModel):
    """Schema for conversation history"""
    id: int
    message: str
    response: str
    provider: str
    model: str
    tokens_used: int
    cost: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Schema for list of conversations"""
    conversations: List[ConversationHistory]
    total: int