from fastapi import APIRouter
from schemas.article import SummarizeRequest, SummarizeResponse
from services.deepseek import deepseek_service
from core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/summarize", tags=["summarize"])

@router.post("/", response_model=SummarizeResponse)
def summarize_article(request: SummarizeRequest):
    """
    Summarize an article and suggest a title and category using DeepSeek LLM.
    
    Args:
        request: SummarizeRequest containing article text
        
    Returns:
        SummarizeResponse with generated title, summary, and category
    """
    logger.info("Received article summarization request")
    
    try:
        result = deepseek_service.analyze_article(request.article_text)
        logger.info(f"Article summarized successfully: {result['title']}")
        return SummarizeResponse(**result)
    except Exception as e:
        logger.error(f"Article summarization failed: {str(e)}")
        raise 