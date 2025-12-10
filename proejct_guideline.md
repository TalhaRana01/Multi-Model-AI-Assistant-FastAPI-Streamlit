```bash 
ai-assistant/
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI entry point
│
│   ├── api/                        # FASTAPI Backend
│   │   ├── __init__.py
│   │   ├── server.py               # FastAPI app instance
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Login/Register JWT endpoints
│   │   │   ├── chat.py             # LLM chat API endpoint
│   │   │   └── health.py           # Health check
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth_schemas.py     # User schema / Tokens schema
│   │   │   └── chat_schemas.py     # Request/response models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py     # Hashing, JWT create/verify
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py         # JWT, password hashing
│   │   │   └── dependencies.py     # Auth dependencies
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── db.py               # DB Session
│   │       └── models.py           # User model
│
│   ├── streamlit_app/              # STREAMLIT UI
│   │   ├── __init__.py
│   │   └── app.py                  # Streamlit UI
│
│   ├── llm/                         # LLM Providers Abstraction Layer
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── openai_provider.py
│   │   └── anthropic_provider.py
│
│   ├── utils/                       # Utility Layer
│   │   ├── __init__.py
│   │   ├── cost_tracker.py
│   │   ├── conversation.py
│   │   └── logger.py
│
│   ├── config.py                    # Pydantic Settings
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_llm_providers.py
│   ├── test_cost_tracker.py
│   ├── test_auth.py
│   └── test_routes.py
│
├── ui/                               # Optional: Streamlit static assets
│   └── README.md
│
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
