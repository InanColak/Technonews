# 📰 Technonews - AI-Powered News Aggregator

A modern news aggregation platform that fetches real-time news from multiple RSS feeds and provides AI-powered topic filtering and summarization.

## 🚀 Features

- **Real-time RSS Feed Aggregation** - Fetches news from multiple tech sources
- **AI-Powered Topic Filtering** - Find news articles by theme/topic
- **Modern Web Interface** - Clean, responsive frontend
- **FastAPI Backend** - High-performance async API
- **SQLite Database** - Local data storage
- **DeepSeek AI Integration** - Advanced summarization capabilities

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/technonews.git
   cd technonews
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🔐 Security Configuration

### Environment Variables Setup

1. **Copy the environment template**
   ```bash
   cp env.example .env
   ```

2. **Configure your API keys in `.env`**
   ```bash
   # Get your DeepSeek API key from: https://platform.deepseek.com/
   DEEPSEEK_API_KEY=your_actual_deepseek_api_key_here
   
   # Generate a secure secret key for production
   SECRET_KEY=your_generated_secret_key_here
   ```

3. **Generate a secure secret key** (for production):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### ⚠️ Security Best Practices

- **NEVER commit `.env` files to version control**
- **Use different API keys for development/production**
- **Rotate API keys regularly**
- **Use environment variables in production deployments**

## 🏃‍♂️ Running the Application

1. **Start the backend server**
   ```bash
   python main.py
   ```

2. **Access the application**
   - **Web Interface**: http://localhost:8000/
   - **API Documentation**: http://localhost:8000/docs
   - **API Status**: http://localhost:8000/api/

## 📱 **How to Use Technonews**

### **👤 For End Users**
📖 **[Read the Complete User Guide](USER_GUIDE.md)** - Everything you need to know about using Technonews!

**Quick Start:**
1. Open http://localhost:8000/ in your browser
2. Enter a topic in the search box (e.g., "AI", "Tesla", "cryptocurrency")
3. Click "Get News" or use the quick topic buttons
4. Browse through the latest relevant articles

### **🔧 For Developers**
- **Interactive API Docs**: http://localhost:8000/docs
- **API Endpoints**: See [API section](#-api-endpoints) below
- **Extend feeds**: Edit `feeds.json` to add more RSS sources

## 🔧 Configuration

### RSS Feeds
Edit `feeds.json` to add/remove RSS feeds:
```json
{
  "feeds": [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://feeds.arstechnica.com/arstechnica/index"
  ],
  "websites": [
    "https://techcrunch.com",
    "https://wired.com"
  ]
}
```

### Environment Variables
All configuration via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API key (required) | - |
| `DEEPSEEK_API_URL` | DeepSeek API endpoint | https://api.deepseek.com/v1/chat/completions |
| `DATABASE_URL` | Database connection string | sqlite:///./technonews.db |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000,http://127.0.0.1:3000 |
| `SECRET_KEY` | Security secret key | (generate for production) |

## 🌐 API Endpoints

- `GET /` - Web interface (redirects to frontend)
- `GET /api/` - API status and endpoints
- `GET /news/{theme}` - Get news by topic/theme
- `POST /summarize` - Summarize article text
- `GET /feeds` - Get RSS feeds configuration
- `GET /articles` - Get stored articles

## 🚀 Deployment

### Production Environment Variables

Set these in your hosting platform (Heroku, Railway, etc.):

```bash
DEEPSEEK_API_KEY=your_production_api_key
SECRET_KEY=your_generated_secure_key
DATABASE_URL=your_production_database_url
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 📝 Development

### Project Structure
```
technonews/
├── core/              # Core configuration and utilities
├── models/            # Database models
├── routers/           # API route handlers
├── services/          # Business logic and external services
├── static/            # Frontend files
├── feeds.json         # RSS feeds configuration
├── main.py           # Application entry point
└── requirements.txt   # Python dependencies
```

### Adding New Features
1. Create new router in `routers/`
2. Add business logic in `services/`
3. Update database models in `models/`
4. Include router in `main.py`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/technonews/issues)
- **Documentation**: [API Docs](http://localhost:8000/docs)

---

⭐ **Star this repo if you find it helpful!** 