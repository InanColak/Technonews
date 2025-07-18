from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class SummarizeRequest(BaseModel):
    """Request model for article summarization."""
    article_text: str

class SummarizeResponse(BaseModel):
    """Response model for article summarization."""
    title: str
    summary: str
    category: str

class StoreArticleRequest(BaseModel):
    """Request model for storing an article."""
    title: str
    summary: str
    category: str
    source_url: str
    timestamp: Optional[datetime] = None  # Optional, defaults to now if not provided

class StoreArticleResponse(BaseModel):
    """Response model for storing an article."""
    id: int
    timestamp: datetime

class FeedbackRequest(BaseModel):
    """Request model for submitting article feedback."""
    article_id: int
    feedback: Literal["like", "dislike"]

class ArticleResponse(BaseModel):
    """Response model for article data."""
    id: int
    title: str
    summary: str
    category: str
    source_url: str
    timestamp: str  # ISO format string

class FeedsResponse(BaseModel):
    """Response model for feeds configuration."""
    feeds: list[str]
    websites: list[str]

class NewsArticle(BaseModel):
    """Response model for a news article from RSS feeds."""
    title: str
    summary: str
    link: str
    published: str
    source: str
    source_url: str

class NewsResponse(BaseModel):
    """Response model for themed news articles."""
    theme: str
    articles: list[NewsArticle]
    total_found: int

class TrendingTopicsResponse(BaseModel):
    """Response model for trending topics."""
    topics: list[str] 