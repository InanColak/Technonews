import requests
import json
from typing import Dict
from fastapi import HTTPException
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

class DeepSeekService:
    """Service for interacting with DeepSeek API for article analysis."""
    
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = settings.deepseek_api_url
        
    def analyze_article(self, article_text: str) -> Dict[str, str]:
        """
        Analyze article text using DeepSeek API to generate title, summary, and category.
        
        Args:
            article_text: Raw article content to analyze
            
        Returns:
            Dictionary with title, summary, and category
            
        Raises:
            HTTPException: If API call fails or response cannot be parsed
        """
        if not self.api_key:
            logger.critical("DeepSeek API key not set in environment variables.")
            raise RuntimeError("DeepSeek API key not set in environment variables.")

        prompt = (
            "You are an expert news assistant. Given the following article, generate a concise, engaging title, "
            "a 2-3 sentence summary, and suggest a category (e.g., politics, technology, health, etc.). "
            "Return the result as a JSON object with keys: title, summary, category.\n\nArticle:\n" + article_text
        )
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }
        
        try:
            logger.info("Calling DeepSeek API for article analysis")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            logger.info(f"DeepSeek API response status: {response.status_code}")
        except requests.exceptions.Timeout:
            logger.error("DeepSeek API request timed out")
            raise HTTPException(
                status_code=504, 
                detail="DeepSeek API request timed out. Please try again later."
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API request failed: {str(e)}")
            raise HTTPException(
                status_code=502, 
                detail=f"DeepSeek API request failed: {str(e)}"
            )
        
        if response.status_code != 200:
            logger.error(f"DeepSeek API error: {response.text}")
            raise HTTPException(
                status_code=502, 
                detail=f"DeepSeek API error: {response.text}"
            )
        
        try:
            result_text = response.json()['choices'][0]['message']['content']
            result = json.loads(result_text)
            logger.info(f"DeepSeek analysis result: {result}")
            
            return {
                "title": result.get("title", ""),
                "summary": result.get("summary", ""),
                "category": result.get("category", "Uncategorized")
            }
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse DeepSeek response. result_text: {result_text}, error: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to parse DeepSeek response as JSON. The model may have returned unexpected output. Error: {str(e)}"
            )

# Create global service instance
deepseek_service = DeepSeekService() 