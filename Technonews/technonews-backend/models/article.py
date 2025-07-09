from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from models.database import Base

class Article(Base):
    """SQLAlchemy model for storing news articles."""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)  # type: ignore
    title = Column(String(256), nullable=False)  # type: ignore
    summary = Column(Text, nullable=False)  # type: ignore
    category = Column(String(64), nullable=False)  # type: ignore
    source_url = Column(String(512), nullable=False)  # type: ignore
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # type: ignore

class Feedback(Base):
    """SQLAlchemy model for storing user feedback on articles."""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)  # type: ignore
    article_id = Column(Integer, nullable=False)  # type: ignore
    feedback = Column(String(16), nullable=False)  # type: ignore  # 'like' or 'dislike'
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # type: ignore 