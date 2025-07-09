from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List

from schemas.article import StoreArticleRequest, StoreArticleResponse, ArticleResponse
from models.article import Article
from models.database import get_db
from core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["articles"])

@router.post("/store", response_model=StoreArticleResponse)
def store_article(request: StoreArticleRequest, db: Session = Depends(get_db)):
    """
    Store an article in the database.
    
    Args:
        request: StoreArticleRequest containing article data
        db: Database session
        
    Returns:
        StoreArticleResponse with stored article ID and timestamp
    """
    logger.info(f"Storing article: {request.title}")
    
    try:
        article = Article(
            title=request.title,
            summary=request.summary,
            category=request.category,
            source_url=request.source_url,
            timestamp=request.timestamp or datetime.utcnow()
        )
        
        db.add(article)
        db.commit()
        db.refresh(article)
        
        logger.info(f"Article stored successfully with ID: {article.id}")
        return StoreArticleResponse(id=article.id, timestamp=article.timestamp)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store article: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store article.")

@router.get("/articles", response_model=List[ArticleResponse])
def get_articles(db: Session = Depends(get_db)):
    """
    Get all articles from the database, ordered by most recent first.
    
    Args:
        db: Database session
        
    Returns:
        List of ArticleResponse objects
    """
    logger.info("Retrieving all articles")
    
    try:
        articles = db.query(Article).order_by(desc(Article.timestamp)).all()
        logger.info(f"Retrieved {len(articles)} articles")
        
        return [
            ArticleResponse(
                id=a.id,
                title=a.title,
                summary=a.summary,
                category=a.category,
                source_url=a.source_url,
                timestamp=a.timestamp.isoformat()
            )
            for a in articles
        ]
        
    except Exception as e:
        logger.error(f"Failed to retrieve articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve articles.") 