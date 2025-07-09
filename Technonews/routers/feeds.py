from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from schemas.article import FeedsResponse
from services.feeds import feeds_service
from core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/feeds", tags=["feeds"])

class UpdateFeedsRequest(BaseModel):
    """Request model for updating feeds configuration."""
    feeds: List[str]
    websites: List[str] = []

class AddFeedRequest(BaseModel):
    """Request model for adding a single feed."""
    feed_url: str

@router.get("/", response_model=FeedsResponse)
def get_feeds():
    """
    Get the current list of RSS feeds and websites from feeds.json.
    
    Returns:
        FeedsResponse with current feeds and websites
    """
    logger.info("Retrieving feeds configuration")
    
    try:
        result = feeds_service.read_feeds()
        logger.info(f"Retrieved {len(result['feeds'])} feeds and {len(result['websites'])} websites")
        return FeedsResponse(**result)
        
    except Exception as e:
        logger.error(f"Failed to retrieve feeds: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve feeds configuration.")

@router.put("/", response_model=FeedsResponse)
def update_feeds(request: UpdateFeedsRequest):
    """
    Update the entire feeds configuration.
    
    Args:
        request: UpdateFeedsRequest with new feeds and websites
        
    Returns:
        FeedsResponse with updated configuration
    """
    logger.info(f"Updating feeds configuration with {len(request.feeds)} feeds and {len(request.websites)} websites")
    
    try:
        feeds_service.write_feeds(request.feeds, request.websites)
        result = feeds_service.read_feeds()
        logger.info("Feeds configuration updated successfully")
        return FeedsResponse(**result)
        
    except Exception as e:
        logger.error(f"Failed to update feeds: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update feeds configuration.")

@router.post("/add")
def add_feed(request: AddFeedRequest):
    """
    Add a new RSS feed to the configuration.
    
    Args:
        request: AddFeedRequest with feed URL to add
        
    Returns:
        Success message
    """
    logger.info(f"Adding new feed: {request.feed_url}")
    
    try:
        success = feeds_service.add_feed(request.feed_url)
        if success:
            return {"status": "success", "message": f"Feed added: {request.feed_url}"}
        else:
            return {"status": "warning", "message": f"Feed already exists: {request.feed_url}"}
            
    except Exception as e:
        logger.error(f"Failed to add feed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add feed.")

@router.delete("/remove")
def remove_feed(request: AddFeedRequest):
    """
    Remove an RSS feed from the configuration.
    
    Args:
        request: AddFeedRequest with feed URL to remove
        
    Returns:
        Success message
    """
    logger.info(f"Removing feed: {request.feed_url}")
    
    try:
        success = feeds_service.remove_feed(request.feed_url)
        if success:
            return {"status": "success", "message": f"Feed removed: {request.feed_url}"}
        else:
            return {"status": "warning", "message": f"Feed not found: {request.feed_url}"}
            
    except Exception as e:
        logger.error(f"Failed to remove feed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to remove feed.") 