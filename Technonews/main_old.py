import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Optional, Literal
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import json
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from fastapi.middleware.cors import CORSMiddleware

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/completions')

app = FastAPI(title="Technonews Summarizer API")

# CORS middleware for React front-end integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stop app if DEEPSEEK_API_KEY is missing
if not DEEPSEEK_API_KEY:
    logger.critical("DEEPSEEK_API_KEY environment variable is not set. Please set it in your .env file.")
    raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set. Please set it in your .env file.")

class SummarizeRequest(BaseModel):
    article_text: str

class SummarizeResponse(BaseModel):
    title: str
    summary: str
    category: str

class StoreArticleRequest(BaseModel):
    title: str
    summary: str
    category: str
    source_url: str
    timestamp: datetime = None  # Required, defaults to now if not provided

class StoreArticleResponse(BaseModel):
    id: int
    timestamp: datetime

class FeedbackRequest(BaseModel):
    article_id: int
    feedback: Literal["like", "dislike"]

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./technonews.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)  # type: ignore
    title = Column(String(256), nullable=False)  # type: ignore
    summary = Column(Text, nullable=False)  # type: ignore
    category = Column(String(64), nullable=False)  # type: ignore
    source_url = Column(String(512), nullable=False)  # type: ignore
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # type: ignore

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)  # type: ignore
    article_id = Column(Integer, nullable=False)  # type: ignore
    feedback = Column(String(16), nullable=False)  # type: ignore
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # type: ignore

# Create tables
Base.metadata.create_all(bind=engine)

# Modular function to call DeepSeek API for content analysis
def analyze_article_with_deepseek(article_text: str) -> Dict[str, str]:
    if not DEEPSEEK_API_KEY:
        logger.critical("DeepSeek API key not set in environment variables.")
        raise RuntimeError("DeepSeek API key not set in environment variables.")

    prompt = (
        "You are an expert news assistant. Given the following article, generate a concise, engaging title, a 2-3 sentence summary, and suggest a category (e.g., politics, technology, health, etc.). "
        "Return the result as a JSON object with keys: title, summary, category.\n\nArticle:\n" + article_text
    )
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # Adjust model name as needed
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        logger.info(f"DeepSeek API called. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        logger.error("DeepSeek API request timed out.")
        raise HTTPException(status_code=504, detail="DeepSeek API request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        logger.error(f"DeepSeek API request failed: {str(e)}")
        raise HTTPException(status_code=502, detail=f"DeepSeek API request failed: {str(e)}")
    if response.status_code != 200:
        logger.error(f"DeepSeek API error: {response.text}")
        raise HTTPException(status_code=502, detail=f"DeepSeek API error: {response.text}")
    try:
        result_text = response.json()['choices'][0]['message']['content']
        result = json.loads(result_text)
        logger.info(f"DeepSeek result: {result}")
        return {
            "title": result.get("title", ""),
            "summary": result.get("summary", ""),
            "category": result.get("category", "Uncategorized")
        }
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse DeepSeek response as JSON. result_text: {result_text}, error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse DeepSeek response as JSON. The model may have returned unexpected output. Error: {str(e)}")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/summarize", response_model=SummarizeResponse)
def summarize_article(request: SummarizeRequest):
    """Summarize an article and suggest a title and category using DeepSeek LLM."""
    result = analyze_article_with_deepseek(request.article_text)
    return SummarizeResponse(**result)

@app.post("/store", response_model=StoreArticleResponse)
def store_article(request: StoreArticleRequest, db: Session = Depends(get_db)):
    """Store an article in the database."""
    article = Article(
        title=request.title,
        summary=request.summary,
        category=request.category,
        source_url=request.source_url,
        timestamp=request.timestamp or datetime.utcnow()
    )
    db.add(article)
    try:
        db.commit()
        logger.info(f"Article stored: {article.title}")
    except Exception as e:
        db.rollback()
        logger.error(f"DB commit failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store article.")
    db.refresh(article)
    return StoreArticleResponse(id=article.id, timestamp=article.timestamp)

FEEDS_FILE = os.getenv('FEEDS_FILE', 'feeds.json')

def read_feeds_file():
    try:
        with open(FEEDS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # If feeds.json is a list, treat it as feeds only
            if isinstance(data, list):
                return {"feeds": data, "websites": []}
            # If feeds.json is a dict, expect 'feeds' and 'websites' keys
            feeds = data.get('feeds', [])
            websites = data.get('websites', [])
            return {"feeds": feeds, "websites": websites}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"feeds.json read error: {str(e)}")
        return {"feeds": [], "websites": []}
    except Exception as e:
        logger.error(f"Unexpected feeds.json error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading feeds.json: {str(e)}")

@app.get("/feeds")
def get_feeds():
    """Return the current list of RSS feeds and websites from feeds.json."""
    return JSONResponse(content=read_feeds_file())

@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    """Return all articles, most recent first."""
    articles = db.query(Article).order_by(desc(Article.timestamp)).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "category": a.category,
            "source_url": a.source_url,
            "timestamp": a.timestamp.isoformat()
        }
        for a in articles
    ]

@app.post("/feedback")
def post_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    """Record user feedback for an article."""
    feedback = Feedback(
        article_id=request.article_id,
        feedback=request.feedback
    )
    db.add(feedback)
    try:
        db.commit()
        logger.info(f"Feedback stored for article_id={request.article_id}, feedback={request.feedback}")
    except Exception as e:
        db.rollback()
        logger.error(f"DB commit failed (feedback): {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store feedback.")
    return {"status": "success"} 