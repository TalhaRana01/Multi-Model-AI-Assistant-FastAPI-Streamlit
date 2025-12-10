"""
Cost tracking utility for LLM usage
"""
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.database.models import Conversation


class CostTracker:
    """Track and analyze LLM usage costs"""
    
    @staticmethod
    def get_total_cost(db: Session, user_id: int = None) -> float:
        """Get total cost for user or all users"""
        query = db.query(func.sum(Conversation.cost))
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        result = query.scalar()
        return round(result or 0.0, 6)
    
    @staticmethod
    def get_cost_by_provider(db: Session, user_id: int = None) -> Dict[str, float]:
        """Get costs grouped by provider"""
        query = db.query(
            Conversation.provider,
            func.sum(Conversation.cost).label('total_cost')
        )
        
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        query = query.group_by(Conversation.provider)
        
        results = query.all()
        return {row.provider: round(row.total_cost, 6) for row in results}
    
    @staticmethod
    def get_cost_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        user_id: int = None
    ) -> List[Dict]:
        """Get costs within date range"""
        query = db.query(Conversation).filter(
            Conversation.created_at >= start_date,
            Conversation.created_at <= end_date
        )
        
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        conversations = query.all()
        
        return [
            {
                "date": conv.created_at.date(),
                "provider": conv.provider,
                "cost": conv.cost,
                "tokens": conv.tokens_used
            }
            for conv in conversations
        ]
    
    @staticmethod
    def get_usage_stats(db: Session, user_id: int = None) -> Dict:
        """Get comprehensive usage statistics"""
        query = db.query(Conversation)
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        
        conversations = query.all()
        
        if not conversations:
            return {
                "total_conversations": 0,
                "total_cost": 0.0,
                "total_tokens": 0,
                "avg_cost_per_conversation": 0.0,
                "by_provider": {}
            }
        
        total_cost = sum(c.cost for c in conversations)
        total_tokens = sum(c.tokens_used for c in conversations)
        
        by_provider = {}
        for conv in conversations:
            if conv.provider not in by_provider:
                by_provider[conv.provider] = {"count": 0, "cost": 0.0, "tokens": 0}
            by_provider[conv.provider]["count"] += 1
            by_provider[conv.provider]["cost"] += conv.cost
            by_provider[conv.provider]["tokens"] += conv.tokens_used
        
        return {
            "total_conversations": len(conversations),
            "total_cost": round(total_cost, 6),
            "total_tokens": total_tokens,
            "avg_cost_per_conversation": round(total_cost / len(conversations), 6),
            "by_provider": by_provider
        }