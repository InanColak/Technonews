# 📱 Technonews User Guide

Welcome to **Technonews** - Your AI-powered news aggregator! This guide will help you get the most out of the application.

## 🌐 **Web Interface Usage**

### **Accessing the Application**
1. Open your web browser
2. Navigate to: **http://localhost:8000/**
3. You'll see the Technonews homepage with a clean, modern interface

### **🔍 Searching for News**

#### **Method 1: Search Box**
1. **Enter a topic** in the search box (e.g., "AI", "Tesla", "cryptocurrency")
2. **Click "Get News"** button
3. Wait for results to load (usually 2-5 seconds)
4. Browse through the relevant articles

#### **Method 2: Quick Topic Buttons**
Click any of the pre-configured topic buttons:
- **AI** - Artificial Intelligence news
- **Tesla** - Tesla and electric vehicle news
- **Crypto** - Cryptocurrency and blockchain news
- **Health** - Health and medical technology
- **Tech** - General technology news
- **Trending** - Popular topics

### **📖 Reading Articles**
Each article card shows:
- **Title** (clickable link to original article)
- **Publication date and source**
- **Summary/excerpt**
- **Direct link** to read the full article

---

## 🔧 **API Usage** 

For developers or advanced users who want to integrate with the API:

### **Base URL**
```
http://localhost:8000
```

### **Available Endpoints**

#### **1. Get News by Topic**
```http
GET /news/{topic}
```

**Example:**
```bash
curl "http://localhost:8000/news/AI"
curl "http://localhost:8000/news/cryptocurrency"
curl "http://localhost:8000/news/Tesla"
```

**Response:**
```json
{
  "theme": "AI",
  "total_found": 15,
  "articles": [
    {
      "title": "Latest AI Breakthrough...",
      "url": "https://techcrunch.com/article...",
      "summary": "Description of the article...",
      "published": "2024-01-15T10:30:00",
      "source": "TechCrunch"
    }
  ]
}
```

#### **2. Article Summarization** (Requires DeepSeek API Key)
```http
POST /summarize
Content-Type: application/json

{
  "text": "Long article text here...",
  "max_length": 200
}
```

#### **3. Get RSS Feeds Configuration**
```http
GET /feeds
```

#### **4. API Status**
```http
GET /api/
```

---

## 💡 **Tips for Better Results**

### **🎯 Effective Search Terms**
- **Specific topics**: "OpenAI GPT-4", "Tesla Model 3", "Bitcoin price"
- **Technology areas**: "machine learning", "renewable energy", "cybersecurity"
- **Company names**: "Apple", "Google", "Microsoft", "Meta"
- **Industry terms**: "fintech", "biotech", "automotive", "space technology"

### **🏷️ Topic Examples That Work Well**
- **AI & Machine Learning**: "artificial intelligence", "neural networks", "ChatGPT"
- **Crypto**: "Bitcoin", "Ethereum", "blockchain", "DeFi"
- **Tech Companies**: "Apple earnings", "Google AI", "Meta VR"
- **Emerging Tech**: "quantum computing", "autonomous vehicles", "renewable energy"
- **Health Tech**: "digital health", "telemedicine", "medical AI"

---

## ⚙️ **Customizing Your Experience**

### **Adding New RSS Feeds**
If you want to add more news sources, edit the `feeds.json` file:

```json
{
  "feeds": [
    "https://techcrunch.com/feed/",
    "https://your-new-feed.com/rss",
    "https://another-source.com/feed.xml"
  ]
}
```

### **Supported Feed Types**
- RSS 2.0
- Atom feeds
- Most major tech news websites

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **"No news found for topic"**
- ✅ Try broader search terms (e.g., "AI" instead of "GPT-4.5")
- ✅ Check if RSS feeds are working (some may be temporarily down)
- ✅ Try different topic variations

#### **"Error fetching news"**
- ✅ Make sure the server is running (`python main.py`)
- ✅ Check that you're accessing the correct URL (http://localhost:8000)
- ✅ Verify your internet connection

#### **Summarization not working**
- ✅ Set your DeepSeek API key in the `.env` file
- ✅ Check your DeepSeek API quota/credits
- ✅ Ensure the API key is valid

#### **Server won't start**
- ✅ Check Python version (3.8+ required)
- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Check for encoding issues in `.env` file

---

## 🎨 **Features Overview**

### **What Technonews Does**
1. **Real-time Aggregation**: Fetches fresh news from 10+ major tech sources
2. **Smart Filtering**: Uses AI to find articles matching your topics
3. **Clean Interface**: Modern, responsive web design
4. **API Access**: RESTful API for developers
5. **Local Storage**: Saves articles locally for faster access

### **Current News Sources**
- TechCrunch
- Wired
- Ars Technica
- VentureBeat
- The Verge
- Mashable
- ZDNet AI section
- Status feeds from major companies
- And more...

---

## 📊 **Understanding Results**

### **Article Relevance**
Articles are filtered based on:
- **Title matching** your search terms
- **Content relevance** to the topic
- **Recency** (newer articles prioritized)
- **Source reliability**

### **Result Limits**
- Maximum **10 articles** per search (for performance)
- Articles from **last 30 days** (configurable)
- Sorted by **relevance and date**

---

## 🤝 **Getting Help**

### **Support Options**
1. **Check this guide** for common questions
2. **Review the README.md** for technical setup
3. **Check server logs** if you encounter errors
4. **API Documentation**: Visit http://localhost:8000/docs for interactive API docs

### **Reporting Issues**
If you find bugs or have suggestions:
1. Check the application logs
2. Document the exact steps to reproduce
3. Note your operating system and Python version
4. Include any error messages

---

**🚀 Happy news reading! Stay informed with Technonews!** 