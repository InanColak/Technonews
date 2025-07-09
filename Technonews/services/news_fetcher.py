import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime
import re
from fastapi import HTTPException

from services.feeds import feeds_service
from core.logging import get_logger

logger = get_logger(__name__)

class NewsFetcher:
    """Service for fetching and filtering current news from RSS feeds."""
    
    def __init__(self):
        self.feeds_service = feeds_service
        
    def fetch_news_by_theme(self, theme: str, limit: int = 10) -> List[Dict]:
        """
        Fetch current news articles filtered by theme/topic.
        
        Args:
            theme: Topic to search for (e.g., "AI", "Tesla", "cryptocurrency")
            limit: Maximum number of articles to return
            
        Returns:
            List of filtered news articles with title, summary, link, published date
        """
        logger.info(f"Fetching news for theme: {theme}")
        
        # Get configured RSS feeds
        feeds_config = self.feeds_service.read_feeds()
        rss_feeds = feeds_config.get("feeds", [])
        
        if not rss_feeds:
            logger.warning("No RSS feeds configured")
            return []
        
        all_articles = []
        
        # Fetch articles from each RSS feed
        for feed_url in rss_feeds:
            try:
                logger.info(f"Fetching from feed: {feed_url}")
                articles = self._parse_rss_feed(feed_url)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error fetching from {feed_url}: {str(e)}")
                continue
        
        # Filter articles by theme
        filtered_articles = self._filter_by_theme(all_articles, theme)
        
        # Sort by publication date (newest first) and limit results
        filtered_articles.sort(key=lambda x: x.get('published_parsed', datetime.min), reverse=True)
        result = filtered_articles[:limit]
        
        logger.info(f"Found {len(result)} articles for theme '{theme}'")
        return result
    
    def _parse_rss_feed(self, feed_url: str) -> List[Dict]:
        """Parse a single RSS feed and extract articles."""
        try:
            # Set user agent to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Fetch feed with timeout
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse RSS feed
            feed = feedparser.parse(response.content)
            
            articles = []
            for entry in feed.entries:
                article = {
                    'title': getattr(entry, 'title', 'No Title'),
                    'summary': getattr(entry, 'summary', getattr(entry, 'description', 'No Summary')),
                    'link': getattr(entry, 'link', ''),
                    'published': getattr(entry, 'published', ''),
                    'published_parsed': getattr(entry, 'published_parsed', None),
                    'source': feed.feed.get('title', feed_url),
                    'source_url': feed_url
                }
                articles.append(article)
            
            logger.info(f"Parsed {len(articles)} articles from {feed_url}")
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching {feed_url}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {str(e)}")
            return []
    
    def _filter_by_theme(self, articles: List[Dict], theme: str) -> List[Dict]:
        """Filter articles that match the given theme."""
        if not theme:
            return articles
        
        theme_keywords = self._generate_keywords(theme)
        filtered = []
        
        for article in articles:
            # Search in title and summary
            text_to_search = f"{article.get('title', '')} {article.get('summary', '')}".lower()
            
            # Check if any keyword matches
            if any(keyword.lower() in text_to_search for keyword in theme_keywords):
                filtered.append(article)
        
        return filtered
    
    def _generate_keywords(self, theme: str) -> List[str]:
        """Generate search keywords for a given theme."""
        # Start with the theme itself
        keywords = [theme]
        
        # Add common variations and related terms
        theme_lower = theme.lower()
        
        # AI/Technology related terms
        if any(term in theme_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
            keywords.extend(['artificial intelligence', 'machine learning', 'AI', 'ML', 'neural network', 
                           'deep learning', 'chatgpt', 'openai', 'llm', 'automation'])
        
        # Tesla/Electric Vehicle terms
        elif any(term in theme_lower for term in ['tesla', 'electric vehicle', 'ev']):
            keywords.extend(['Tesla', 'electric vehicle', 'EV', 'Elon Musk', 'battery', 'charging', 
                           'electric car', 'automotive'])
        
        # Cryptocurrency terms
        elif any(term in theme_lower for term in ['crypto', 'bitcoin', 'blockchain']):
            keywords.extend(['cryptocurrency', 'bitcoin', 'blockchain', 'crypto', 'BTC', 'ethereum', 
                           'digital currency', 'trading'])
        
        # Technology general terms
        elif any(term in theme_lower for term in ['tech', 'technology', 'startup']):
            keywords.extend(['technology', 'tech', 'startup', 'innovation', 'software', 'hardware'])
        
        # Health terms
        elif any(term in theme_lower for term in ['health', 'medical', 'medicine']):
            keywords.extend(['health', 'medical', 'medicine', 'healthcare', 'treatment', 'research'])
        
        # Remove duplicates and return
        return list(set(keywords))
    
    def get_trending_topics(self) -> List[str]:
        """Get list of trending topics based on recent articles."""
        logger.info("Analyzing trending topics")
        
        feeds_config = self.feeds_service.read_feeds()
        rss_feeds = feeds_config.get("feeds", [])
        
        all_articles = []
        for feed_url in rss_feeds:
            try:
                articles = self._parse_rss_feed(feed_url)
                all_articles.extend(articles[:5])  # Take recent articles from each feed
            except Exception:
                continue
        
        # Simple keyword extraction (can be enhanced with NLP)
        common_words = {}
        for article in all_articles:
            title = article.get('title', '').lower()
            words = re.findall(r'\b\w{4,}\b', title)  # Words with 4+ characters
            for word in words:
                if word not in ['news', 'says', 'will', 'new', 'first', 'more', 'after', 'with']:
                    common_words[word] = common_words.get(word, 0) + 1
        
        # Return top trending words
        trending = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:10]
        return [word for word, count in trending]

# Create global service instance
news_fetcher = NewsFetcher() 