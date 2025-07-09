from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.article import FeedbackRequest
from models.article import Feedback
from models.database import get_db
from core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/")
def post_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    """
    Record user feedback for an article.
    
    Args:
        request: FeedbackRequest containing article ID and feedback
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"Recording feedback for article {request.article_id}: {request.feedback}")
    
    try:
        feedback = Feedback(
            article_id=request.article_id,
            feedback=request.feedback
        )
        
        db.add(feedback)
        db.commit()
        
        logger.info(f"Feedback stored successfully for article {request.article_id}")
        return {"status": "success"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store feedback.") 