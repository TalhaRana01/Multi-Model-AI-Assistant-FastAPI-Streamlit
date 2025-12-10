"""
Chat/LLM interaction routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from ..schemas.chat_schemas import (
    ChatRequest, 
    ChatResponse, 
    ConversationHistory,
    ConversationListResponse
)
from ..database.db import get_db
from ..database.models import User, Conversation
from ..core.dependencies import get_current_user
from ...llm.openai_provider import OpenAIProvider
from ...llm.anthropic_provider import AnthropicProvider
from ...config import settings
from ...utils.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_llm_provider(provider: str, model: str = None):
    """Get LLM provider instance"""
    if provider == "openai":
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured"
            )
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=model or "gpt-3.5-turbo"
        )
    
    elif provider == "anthropic":
        if not settings.anthropic_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Anthropic API key not configured"
            )
        return AnthropicProvider(
            api_key=settings.anthropic_api_key,
            model=model or "claude-3-haiku-20240307"
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider: {provider}"
        )


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to LLM and get response"""
    try:
        # Get provider
        provider = get_llm_provider(request.provider, request.model)
        
        # Generate response
        result = provider.generate_response(
            prompt=request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Save to database
        conversation = Conversation(
            user_id=current_user.id,
            message=request.message,
            response=result["response"],
            provider=provider.get_provider_name(),
            model=provider.model,
            tokens_used=result["tokens_used"],
            cost=result["cost"]
        )
        
        db.add(conversation)
        db.commit()
        
        logger.info(f"Chat completed for user {current_user.username}: {result['tokens_used']} tokens, ${result['cost']}")
        
        return ChatResponse(
            response=result["response"],
            provider=provider.get_provider_name(),
            model=provider.model,
            tokens_used=result["tokens_used"],
            cost=result["cost"],
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


@router.get("/history", response_model=ConversationListResponse)
async def get_conversation_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation history for current user"""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).offset(offset).limit(limit).all()
    
    total = db.query(Conversation).filter(Conversation.user_id == current_user.id).count()
    
    return ConversationListResponse(
        conversations=conversations,
        total=total
    )