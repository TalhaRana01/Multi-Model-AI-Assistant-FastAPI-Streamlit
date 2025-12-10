"""
OpenAI LLM Provider implementation
"""
from typing import Dict, Any
import openai
from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider implementation"""
    
    # Pricing per 1K tokens (approximate)
    PRICING = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03}
    }
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        openai.api_key = api_key
    
    def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = self.calculate_cost(tokens_used)
            
            return {
                "response": content,
                "tokens_used": tokens_used,
                "cost": cost
            }
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Return provider name"""
        return "openai"
    
    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate approximate cost"""
        pricing = self.PRICING.get(self.model, self.PRICING["gpt-3.5-turbo"])
        # Rough estimate: 75% input, 25% output
        input_tokens = int(tokens_used * 0.75)
        output_tokens = tokens_used - input_tokens
        
        cost = (input_tokens / 1000 * pricing["input"]) + \
               (output_tokens / 1000 * pricing["output"])
        return round(cost, 6)