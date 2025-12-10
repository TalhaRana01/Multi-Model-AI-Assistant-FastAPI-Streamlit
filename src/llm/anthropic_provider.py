"""
Anthropic Claude LLM Provider implementation
"""
from typing import Dict, Any
import anthropic
from .base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider implementation"""
    
    # Pricing per 1M tokens (approximate)
    PRICING = {
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-opus": {"input": 15.0, "output": 75.0}
    }
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        super().__init__(api_key, model)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Anthropic API"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = message.content[0].text
            tokens_used = message.usage.input_tokens + message.usage.output_tokens
            cost = self.calculate_cost(tokens_used)
            
            return {
                "response": content,
                "tokens_used": tokens_used,
                "cost": cost
            }
        
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Return provider name"""
        return "anthropic"
    
    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate approximate cost"""
        # Determine model family
        model_family = "claude-3-haiku"
        if "sonnet" in self.model:
            model_family = "claude-3-sonnet"
        elif "opus" in self.model:
            model_family = "claude-3-opus"
        
        pricing = self.PRICING.get(model_family, self.PRICING["claude-3-haiku"])
        
        # Rough estimate: 75% input, 25% output
        input_tokens = int(tokens_used * 0.75)
        output_tokens = tokens_used - input_tokens
        
        cost = (input_tokens / 1_000_000 * pricing["input"]) + \
               (output_tokens / 1_000_000 * pricing["output"])
        return round(cost, 6)