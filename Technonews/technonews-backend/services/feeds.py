import json
from typing import Dict, List
from fastapi import HTTPException
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

class FeedsService:
    """Service for managing RSS feeds and website configuration."""
    
    def __init__(self):
        self.feeds_file = settings.feeds_file
        
    def read_feeds(self) -> Dict[str, List[str]]:
        """
        Read feeds configuration from feeds.json file.
        
        Returns:
            Dictionary with 'feeds' and 'websites' lists
            
        Raises:
            HTTPException: If unexpected error occurs reading file
        """
        try:
            logger.info(f"Reading feeds configuration from {self.feeds_file}")
            with open(self.feeds_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle both list and dict formats
            if isinstance(data, list):
                logger.info(f"Found {len(data)} feeds in list format")
                return {"feeds": data, "websites": []}
            
            feeds = data.get('feeds', [])
            websites = data.get('websites', [])
            logger.info(f"Found {len(feeds)} feeds and {len(websites)} websites")
            
            return {"feeds": feeds, "websites": websites}
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading feeds file: {str(e)}")
            return {"feeds": [], "websites": []}
        except Exception as e:
            logger.error(f"Unexpected error reading feeds file: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error reading feeds.json: {str(e)}"
            )
    
    def write_feeds(self, feeds: List[str], websites: List[str] = None) -> bool:
        """
        Write feeds configuration to feeds.json file.
        
        Args:
            feeds: List of RSS feed URLs
            websites: List of website URLs (optional)
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If writing fails
        """
        if websites is None:
            websites = []
            
        data = {
            "feeds": feeds,
            "websites": websites
        }
        
        try:
            logger.info(f"Writing {len(feeds)} feeds and {len(websites)} websites to {self.feeds_file}")
            with open(self.feeds_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info("Feeds configuration updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error writing feeds file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error writing feeds.json: {str(e)}"
            )
    
    def add_feed(self, feed_url: str) -> bool:
        """
        Add a new RSS feed URL to the configuration.
        
        Args:
            feed_url: RSS feed URL to add
            
        Returns:
            True if successful
        """
        current = self.read_feeds()
        feeds = current["feeds"]
        websites = current["websites"]
        
        if feed_url not in feeds:
            feeds.append(feed_url)
            self.write_feeds(feeds, websites)
            logger.info(f"Added new feed: {feed_url}")
            return True
        else:
            logger.warning(f"Feed already exists: {feed_url}")
            return False
    
    def remove_feed(self, feed_url: str) -> bool:
        """
        Remove an RSS feed URL from the configuration.
        
        Args:
            feed_url: RSS feed URL to remove
            
        Returns:
            True if successful
        """
        current = self.read_feeds()
        feeds = current["feeds"]
        websites = current["websites"]
        
        if feed_url in feeds:
            feeds.remove(feed_url)
            self.write_feeds(feeds, websites)
            logger.info(f"Removed feed: {feed_url}")
            return True
        else:
            logger.warning(f"Feed not found: {feed_url}")
            return False

# Create global service instance
feeds_service = FeedsService() 