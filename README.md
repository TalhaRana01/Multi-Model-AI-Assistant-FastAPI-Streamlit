# 🤖 AI Assistant - Multi-LLM Platform

A production-ready AI assistant with FastAPI backend, Streamlit UI, JWT authentication, and support for multiple LLM providers (OpenAI & Anthropic).

## 📋 Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 🤖 **Multiple LLM Providers** - Support for OpenAI GPT and Anthropic Claude
- 💬 **Interactive Chat UI** - Beautiful Streamlit interface
- 📊 **Cost Tracking** - Monitor token usage and costs
- 📝 **Conversation History** - Save and retrieve chat history
- 🔌 **RESTful API** - FastAPI backend with automatic docs
- 🗃️ **Database** - SQLAlchemy with SQLite (easily switchable to PostgreSQL)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository>
cd ai-assistant
```

### 2. Install Dependencies

Using UV (recommended):
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

Using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=your-secret-key-here
```

### 4. Initialize Database

```bash
python -m src.main init-db
```

### 5. Run the Application

**Option A: Run API and UI separately**

Terminal 1 - Start API:
```bash
python -m src.main serve --reload
```

Terminal 2 - Start UI:
```bash
python -m src.main ui
```

**Option B: Run both with one command**

```bash
# In one terminal
python -m src.main serve --reload &
python -m src.main ui
```

Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501

## 📚 API Documentation

### Authentication Endpoints

**Register User**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123"
  }'
```

**Login**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "secure123"
  }'
```

**Get Current User**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Chat Endpoints

**Send Message**
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, AI!",
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

**Get Conversation History**
```bash
curl -X GET "http://localhost:8000/chat/history?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🏗️ Project Structure

```
ai-assistant/
├── src/
│   ├── api/                    # FastAPI Backend
│   │   ├── routes/            # API endpoints
│   │   ├── schemas/           # Pydantic models
│   │   ├── services/          # Business logic
│   │   ├── core/              # Security & dependencies
│   │   ├── database/          # Database models
│   │   └── server.py          # FastAPI app
│   ├── streamlit_app/         # Streamlit UI
│   ├── llm/                   # LLM providers
│   ├── utils/                 # Utilities
│   ├── config.py              # Configuration
│   └── main.py                # CLI entry point
├── tests/                     # Tests
├── pyproject.toml            # Project config
└── .env                      # Environment variables
```

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## 🔧 Configuration

Key settings in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `ANTHROPIC_API_KEY` | Anthropic API key | None |
| `SECRET_KEY` | JWT secret key | Change in production! |
| `DATABASE_URL` | Database connection | sqlite:///./ai_assistant.db |
| `API_PORT` | API server port | 8000 |
| `STREAMLIT_PORT` | UI port | 8501 |

## 🗄️ Database

Default: SQLite (file-based)

Switch to PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📊 Cost Tracking

The system automatically tracks:
- Tokens used per conversation
- Estimated costs
- Provider-wise breakdown
- Historical usage

Access via the Streamlit UI sidebar or API endpoints.

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- 30-minute token expiration (configurable)
- CORS protection
- Input validation with Pydantic

## 🚢 Production Deployment

1. **Set secure SECRET_KEY**
2. **Use PostgreSQL** instead of SQLite
3. **Configure CORS** properly in `server.py`
4. **Use HTTPS** with reverse proxy (nginx/traefik)
5. **Set DEBUG=False**
6. **Use gunicorn** for production:

```bash
gunicorn src.api.server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Available Models

**OpenAI:**
- gpt-3.5-turbo (cheapest, fastest)
- gpt-4
- gpt-4-turbo

**Anthropic:**
- claude-3-haiku-20240307 (fastest)
- claude-3-sonnet-20240229 (balanced)
- claude-3-opus-20240229 (most capable)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Documentation: http://localhost:8000/docs
- Issues: GitHub Issues
- Email: your.email@example.com

## 🎯 Roadmap

- [ ] Support for more LLM providers (Cohere, Mistral)
- [ ] Streaming responses
- [ ] Image generation support
- [ ] Voice input/output
- [ ] Multi-user chat rooms
- [ ] Admin dashboard
- [ ] Rate limiting
- [ ] Webhooks

---

Made with ❤️ by Talha Rana