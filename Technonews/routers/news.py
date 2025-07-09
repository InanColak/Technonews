from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from schemas.article import NewsResponse, NewsArticle, TrendingTopicsResponse
from services.news_fetcher import news_fetcher
from core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{theme}", response_model=NewsResponse)
def get_news_by_theme(
    theme: str, 
    limit: int = Query(default=10, ge=1, le=50, description="Number of articles to return")
):
    """
    Get current news articles filtered by theme/topic from configured RSS feeds.
    
    Args:
        theme: Topic to search for (e.g., "AI", "Tesla", "cryptocurrency", "health")
        limit: Maximum number of articles to return (1-50)
        
    Returns:
        NewsResponse with filtered articles and metadata
        
    Examples:
        - /news/AI
        - /news/Tesla
        - /news/cryptocurrency
        - /news/health?limit=5
    """
    logger.info(f"Fetching news for theme: {theme}")
    
    try:
        # Fetch articles from RSS feeds
        articles_data = news_fetcher.fetch_news_by_theme(theme, limit)
        
        # Convert to response models
        articles = []
        for article_data in articles_data:
            article = NewsArticle(
                title=article_data.get('title', 'No Title'),
                summary=article_data.get('summary', 'No Summary'),
                link=article_data.get('link', ''),
                published=article_data.get('published', ''),
                source=article_data.get('source', 'Unknown'),
                source_url=article_data.get('source_url', '')
            )
            articles.append(article)
        
        logger.info(f"Successfully fetched {len(articles)} articles for theme '{theme}'")
        
        return NewsResponse(
            theme=theme,
            articles=articles,
            total_found=len(articles)
        )
        
    except Exception as e:
        logger.error(f"Error fetching news for theme '{theme}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch news for theme '{theme}': {str(e)}"
        )

@router.get("/", response_model=TrendingTopicsResponse)
def get_trending_topics():
    """
    Get trending topics based on current news from RSS feeds.
    
    Returns:
        TrendingTopicsResponse with list of trending topic keywords
    """
    logger.info("Fetching trending topics")
    
    try:
        topics = news_fetcher.get_trending_topics()
        logger.info(f"Found {len(topics)} trending topics")
        
        return TrendingTopicsResponse(topics=topics)
        
    except Exception as e:
        logger.error(f"Error fetching trending topics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trending topics: {str(e)}"
        )

@router.get("/search/{keyword}", response_model=NewsResponse)
def search_news(
    keyword: str,
    limit: int = Query(default=10, ge=1, le=50, description="Number of articles to return")
):
    """
    Search for news articles containing specific keywords.
    
    Args:
        keyword: Keyword to search for in article titles and summaries
        limit: Maximum number of articles to return (1-50)
        
    Returns:
        NewsResponse with matching articles
    """
    logger.info(f"Searching news for keyword: {keyword}")
    
    try:
        # Use the same theme filtering but with exact keyword
        articles_data = news_fetcher.fetch_news_by_theme(keyword, limit)
        
        # Convert to response models
        articles = []
        for article_data in articles_data:
            article = NewsArticle(
                title=article_data.get('title', 'No Title'),
                summary=article_data.get('summary', 'No Summary'),
                link=article_data.get('link', ''),
                published=article_data.get('published', ''),
                source=article_data.get('source', 'Unknown'),
                source_url=article_data.get('source_url', '')
            )
            articles.append(article)
        
        logger.info(f"Found {len(articles)} articles for keyword '{keyword}'")
        
        return NewsResponse(
            theme=keyword,
            articles=articles,
            total_found=len(articles)
        )
        
    except Exception as e:
        logger.error(f"Error searching news for keyword '{keyword}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search news for keyword '{keyword}': {str(e)}"
        ) 