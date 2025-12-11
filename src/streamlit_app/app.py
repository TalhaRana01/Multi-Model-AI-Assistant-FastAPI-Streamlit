"""
Ultra-Professional Streamlit UI for AI Assistant with Stunning Design
"""
import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional
import time

# Configuration
API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# Advanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container with animated gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(30, 60, 114, 0.85);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Enhanced chat messages with glassmorphism */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        padding: 24px !important;
        margin: 16px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stChatMessage:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Animated headers */
    h1, h2, h3 {
        color: white !important;
        font-weight: 800 !important;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    h1 {
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Premium buttons with hover effects */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 14px 24px;
        font-size: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.7);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Elegant input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 14px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: white !important;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Animated metrics */
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: white !important;
        font-size: 14px !important;
    }
    
    /* Success/Error with modern styling */
    .stSuccess {
        background: rgba(76, 175, 80, 0.15) !important;
        border-left: 5px solid #4CAF50 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s ease-out;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.15) !important;
        border-left: 5px solid #F44336 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s ease-out;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.15) !important;
        border-left: 5px solid #FFC107 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Premium tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat input with glow effect */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 25px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Card containers */
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.35);
    }
    
    /* Badge styling */
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0


def login(username: str, password: str) -> bool:
    """Login user"""
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.username = username
            return True
        return False
    except Exception as e:
        st.error(f"🔌 Connection error: {str(e)}")
        return False


def register(username: str, email: str, password: str) -> bool:
    """Register new user"""
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        return response.status_code == 201
    except Exception as e:
        st.error(f"🔌 Connection error: {str(e)}")
        return False


def send_message(message: str, provider: str, model: str, temperature: float, max_tokens: int) -> Optional[dict]:
    """Send message to LLM"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_URL}/chat/",
            headers=headers,
            json={
                "message": message,
                "provider": provider,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return None


def get_history() -> list:
    """Get conversation history"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/chat/history?limit=50", headers=headers)
        if response.status_code == 200:
            return response.json()["conversations"]
        return []
    except:
        return []


def create_cost_chart():
    """Create advanced cost visualization"""
    if not st.session_state.chat_history:
        return None
    
    costs = [msg.get('cost', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
    if not costs:
        return None
        
    timestamps = list(range(1, len(costs) + 1))
    
    fig = go.Figure()
    
    # Main line
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=costs,
        mode='lines+markers',
        name='Cost per message',
        line=dict(color='#667eea', width=3, shape='spline'),
        marker=dict(
            size=10,
            color='#764ba2',
            line=dict(color='white', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    # Cumulative cost
    cumulative = [sum(costs[:i+1]) for i in range(len(costs))]
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=cumulative,
        mode='lines',
        name='Cumulative cost',
        line=dict(color='#f093fb', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title={
            'text': '💰 Cost Analytics',
            'font': {'size': 20, 'color': 'white', 'family': 'Inter'}
        },
        xaxis_title='Message Number',
        yaxis_title='Cost per Message ($)',
        yaxis2=dict(
            title='Cumulative Cost ($)',
            overlaying='y',
            side='right'
        ),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    return fig


def create_token_distribution():
    """Create token usage distribution"""
    if not st.session_state.chat_history:
        return None
        
    tokens = [msg.get('tokens', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
    if not tokens:
        return None
        
    fig = go.Figure(data=[go.Bar(
        x=list(range(1, len(tokens) + 1)),
        y=tokens,
        marker=dict(
            color=tokens,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Tokens")
        )
    )])
    
    fig.update_layout(
        title={
            'text': '🎯 Token Usage Distribution',
            'font': {'size': 20, 'color': 'white', 'family': 'Inter'}
        },
        xaxis_title='Message Number',
        yaxis_title='Tokens Used',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


# Main UI
st.markdown("""
    <div style='text-align: center; padding: 30px 20px;'>
        <h1 style='font-size: 4rem; margin-bottom: 10px; background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🤖 AI Assistant Pro
        </h1>
        <p style='font-size: 1.3rem; color: rgba(255,255,255,0.85); margin-top: 10px; font-weight: 300;'>
            Your Premium Multi-LLM Intelligence Platform
        </p>
        <div style='margin-top: 20px;'>
            <span class='badge'>✨ Powered by GPT-4 & Claude</span>
            <span class='badge'>🚀 Real-time Analytics</span>
            <span class='badge'>🔒 Secure & Private</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Authentication UI
if not st.session_state.token:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])
        
        with tab1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 👋 Welcome Back!")
            st.markdown("<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Sign in to continue your AI journey</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                login_username = st.text_input("👤 Username", placeholder="Enter your username")
                login_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit_login = st.form_submit_button("🚀 Sign In", use_container_width=True)
                
                if submit_login:
                    if login_username and login_password:
                        with st.spinner("🔄 Authenticating..."):
                            if login(login_username, login_password):
                                st.success("✅ Welcome back! Redirecting...")
                                st.balloons()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials. Please try again.")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### ✨ Join AI Assistant Pro")
            st.markdown("<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Create your account in seconds</p>", unsafe_allow_html=True)
            
            with st.form("register_form"):
                reg_username = st.text_input("👤 Username", placeholder="Choose a unique username")
                reg_email = st.text_input("📧 Email", placeholder="your.email@example.com")
                reg_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit_register = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if submit_register:
                    if reg_username and reg_email and reg_password:
                        with st.spinner("🔄 Creating your account..."):
                            if register(reg_username, reg_email, reg_password):
                                st.success("✅ Account created successfully! Please sign in.")
                                st.balloons()
                            else:
                                st.error("❌ Registration failed. Username or email may already exist.")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar for authenticated users
    with st.sidebar:
        st.markdown(f"""
            <div class='card' style='text-align: center; margin-bottom: 25px;'>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 15px;
                            display: flex; align-items: center; justify-content: center;
                            font-size: 36px; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);'>
                    👤
                </div>
                <h2 style='color: white; margin: 0; font-size: 24px;'>{st.session_state.username}</h2>
                <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin-top: 5px;'>Premium Member</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.chat_history = []
            st.session_state.total_cost = 0.0
            st.session_state.total_tokens = 0
            st.rerun()
        
        st.markdown("---")
        
        # Statistics with cards
        st.markdown("### 📊 Session Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "💬 Messages",
                len([m for m in st.session_state.chat_history if m['role'] == 'user']),
                delta=None
            )
        with col2:
            st.metric(
                "💰 Cost",
                f"${st.session_state.total_cost:.4f}",
                delta=None
            )
        
        st.metric(
            "🎯 Tokens",
            f"{st.session_state.total_tokens:,}",
            delta=None
        )
        
        st.markdown("---")
        
        # LLM Settings
        st.markdown("### ⚙️ Model Configuration")
        
        provider = st.selectbox(
            "🤖 AI Provider",
            ["openai", "anthropic"],
            help="Select your preferred AI provider"
        )
        
        if provider == "openai":
            model_options = {
                "GPT-3.5 Turbo ⚡": "gpt-3.5-turbo",
                "GPT-4 🧠": "gpt-4",
                "GPT-4 Turbo 🚀": "gpt-4-turbo"
            }
        else:
            model_options = {
                "Claude 3 Haiku ⚡": "claude-3-haiku-20240307",
                "Claude 3 Sonnet 🎭": "claude-3-sonnet-20240229",
                "Claude 3 Opus 👑": "claude-3-opus-20240229"
            }
        
        model_display = st.selectbox("🎯 Model", list(model_options.keys()))
        model = model_options[model_display]
        
        temperature = st.slider(
            "🌡️ Temperature",
            0.0, 2.0, 0.7, 0.1,
            help="Higher values = more creative | Lower values = more focused"
        )
        
        max_tokens = st.slider(
            "📝 Max Tokens",
            100, 4000, 1000, 100,
            help="Maximum length of the AI response"
        )
        
        st.markdown("---")
        
        # History controls
        st.markdown("### 📚 Conversation History")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Load", use_container_width=True):
                with st.spinner("🔄 Loading history..."):
                    history = get_history()
                    if history:
                        st.session_state.chat_history = []
                        for h in reversed(history):
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": h["message"],
                                "timestamp": h["created_at"]
                            })
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": h["response"],
                                "provider": h["provider"],
                                "model": h["model"],
                                "cost": h["cost"],
                                "tokens": h["tokens_used"]
                            })
                        st.success("✅ History loaded successfully!")
                        time.sleep(0.5)
                        st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.total_cost = 0.0
                st.session_state.total_tokens = 0
                st.rerun()
        
        # Visualizations
        if len([m for m in st.session_state.chat_history if m['role'] == 'assistant']) > 0:
            st.markdown("---")
            st.markdown("### 📈 Analytics Dashboard")
            
            # Cost chart
            fig = create_cost_chart()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Token distribution
            fig2 = create_token_distribution()
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
    
    # Main chat area
    st.markdown("### 💬 AI Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for idx, msg in enumerate(st.session_state.chat_history):
            with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])
                
                if msg["role"] == "assistant" and "cost" in msg:
                    st.markdown(f"""
                        <div class='card' style='margin-top: 15px; padding: 12px;'>
                            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 13px;'>
                                <div>
                                    <span style='color: rgba(255,255,255,0.6);'>Provider:</span>
                                    <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('provider', 'N/A').upper()}</span>
                                </div>
                                <div>
                                    <span style='color: rgba(255,255,255,0.6);'>Model:</span>
                                    <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('model', 'N/A')}</span>
                                </div>
                                <div>
                                    <span style='color: rgba(255,255,255,0.6);'>Tokens:</span>
                                    <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('tokens', 0):,}</span>
                                </div>
                                <div>
                                    <span style='color: rgba(255,255,255,0.6);'>Cost:</span>
                                    <span style='color: white; font-weight: 600; margin-left: 5px;'>${msg.get('cost', 0):.6f}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Chat input at the bottom
    if prompt := st.chat_input("Type your message here...", key="chat_input"):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Thinking..."):
                response = send_message(
                    prompt, 
                    provider, 
                    model, 
                    temperature, 
                    max_tokens
                )
                
                if response:
                    # Display the response
                    st.markdown(response.get("response", "No response received"))
                    
                    # Add assistant message to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response.get("response", ""),
                        "provider": provider,
                        "model": model,
                        "cost": response.get("cost", 0),
                        "tokens": response.get("tokens_used", 0)
                    })
                    
                    # Update totals
                    st.session_state.total_cost += response.get("cost", 0)
                    st.session_state.total_tokens += response.get("tokens_used", 0)
                else:
                    st.error("❌ Failed to get response from AI")



# """
# Ultra-Professional Streamlit UI for AI Assistant with Stunning Design
# """
# import streamlit as st
# import requests
# from datetime import datetime
# import plotly.graph_objects as go
# import plotly.express as px
# from typing import Optional
# import time

# # Configuration
# API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# # Advanced Custom CSS
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
#     * {
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Main container with animated gradient */
#     .main {
#         background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
#         background-size: 400% 400%;
#         animation: gradientShift 15s ease infinite;
#     }
    
#     @keyframes gradientShift {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }
    
#     /* Glassmorphism sidebar */
#     [data-testid="stSidebar"] {
#         background: rgba(30, 60, 114, 0.85);
#         backdrop-filter: blur(20px);
#         border-right: 1px solid rgba(255, 255, 255, 0.1);
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
#     }
    
#     [data-testid="stSidebar"] * {
#         color: white !important;
#     }
    
#     /* Enhanced chat messages with glassmorphism */
#     .stChatMessage {
#         background: rgba(255, 255, 255, 0.1) !important;
#         backdrop-filter: blur(10px);
#         border-radius: 20px !important;
#         padding: 24px !important;
#         margin: 16px 0 !important;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
#         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#     }
    
#     .stChatMessage:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.35);
#         border: 1px solid rgba(255, 255, 255, 0.3);
#     }
    
#     /* Animated headers */
#     h1, h2, h3 {
#         color: white !important;
#         font-weight: 800 !important;
#         text-shadow: 0 4px 12px rgba(0,0,0,0.3);
#         letter-spacing: -0.5px;
#     }
    
#     h1 {
#         animation: fadeInDown 0.8s ease-out;
#     }
    
#     @keyframes fadeInDown {
#         from {
#             opacity: 0;
#             transform: translateY(-30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }
    
#     /* Premium buttons with hover effects */
#     .stButton > button {
#         width: 100%;
#         border-radius: 12px;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         font-weight: 600;
#         border: none;
#         padding: 14px 24px;
#         font-size: 15px;
#         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#         box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
#         position: relative;
#         overflow: hidden;
#     }
    
#     .stButton > button:before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: -100%;
#         width: 100%;
#         height: 100%;
#         background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
#         transition: left 0.5s;
#     }
    
#     .stButton > button:hover:before {
#         left: 100%;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0 10px 30px rgba(102, 126, 234, 0.7);
#     }
    
#     .stButton > button:active {
#         transform: translateY(-1px);
#     }
    
#     /* Elegant input fields */
#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea {
#         border-radius: 12px;
#         border: 2px solid rgba(102, 126, 234, 0.3);
#         padding: 14px;
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         color: white !important;
#         font-size: 15px;
#         transition: all 0.3s ease;
#     }
    
#     .stTextInput > div > div > input:focus,
#     .stTextArea > div > div > textarea:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
#         transform: translateY(-2px);
#     }
    
#     .stTextInput > div > div > input::placeholder,
#     .stTextArea > div > div > textarea::placeholder {
#         color: rgba(255, 255, 255, 0.5) !important;
#     }
    
#     /* Animated metrics */
#     [data-testid="stMetricValue"] {
#         font-size: 32px !important;
#         font-weight: 800 !important;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         animation: pulse 2s ease-in-out infinite;
#     }
    
#     @keyframes pulse {
#         0%, 100% { opacity: 1; }
#         50% { opacity: 0.8; }
#     }
    
#     [data-testid="stMetricLabel"] {
#         font-weight: 600 !important;
#         color: white !important;
#         font-size: 14px !important;
#     }
    
#     /* Success/Error with modern styling */
#     .stSuccess {
#         background: rgba(76, 175, 80, 0.15) !important;
#         border-left: 5px solid #4CAF50 !important;
#         border-radius: 12px !important;
#         backdrop-filter: blur(10px);
#         animation: slideIn 0.5s ease-out;
#     }
    
#     .stError {
#         background: rgba(244, 67, 54, 0.15) !important;
#         border-left: 5px solid #F44336 !important;
#         border-radius: 12px !important;
#         backdrop-filter: blur(10px);
#         animation: slideIn 0.5s ease-out;
#     }
    
#     .stWarning {
#         background: rgba(255, 193, 7, 0.15) !important;
#         border-left: 5px solid #FFC107 !important;
#         border-radius: 12px !important;
#         backdrop-filter: blur(10px);
#     }
    
#     @keyframes slideIn {
#         from {
#             transform: translateX(-20px);
#             opacity: 0;
#         }
#         to {
#             transform: translateX(0);
#             opacity: 1;
#         }
#     }
    
#     /* Premium tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 12px;
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 15px;
#         padding: 8px;
#         backdrop-filter: blur(10px);
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 10px;
#         color: rgba(255, 255, 255, 0.7);
#         font-weight: 600;
#         padding: 12px 24px;
#         transition: all 0.3s ease;
#     }
    
#     .stTabs [data-baseweb="tab"]:hover {
#         background: rgba(255, 255, 255, 0.1);
#         color: white;
#     }
    
#     .stTabs [data-baseweb="tab"][aria-selected="true"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white !important;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
#     }
    
#     /* Chat input with glow effect */
#     .stChatInput > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         backdrop-filter: blur(10px);
#         border-radius: 25px !important;
#         border: 2px solid rgba(102, 126, 234, 0.3) !important;
#         transition: all 0.3s ease;
#     }
    
#     .stChatInput > div:focus-within {
#         border-color: #667eea !important;
#         box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
#     }
    
#     /* Selectbox styling */
#     .stSelectbox > div > div {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         border-radius: 12px;
#         border: 2px solid rgba(102, 126, 234, 0.3);
#     }
    
#     /* Slider styling */
#     .stSlider > div > div > div {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     }
    
#     /* Spinner */
#     .stSpinner > div {
#         border-color: #667eea transparent transparent transparent !important;
#     }
    
#     /* Scrollbar */
#     ::-webkit-scrollbar {
#         width: 10px;
#         height: 10px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
#     }
    
#     /* Card containers */
#     .card {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(20px);
#         border-radius: 20px;
#         padding: 24px;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
#         transition: all 0.3s ease;
#     }
    
#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.35);
#     }
    
#     /* Badge styling */
#     .badge {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 6px 16px;
#         border-radius: 20px;
#         font-size: 13px;
#         font-weight: 600;
#         display: inline-block;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
#         margin: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Page config
# st.set_page_config(
#     page_title="AI Assistant Pro",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize session state
# if 'token' not in st.session_state:
#     st.session_state.token = None
# if 'username' not in st.session_state:
#     st.session_state.username = None
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'total_cost' not in st.session_state:
#     st.session_state.total_cost = 0.0
# if 'total_tokens' not in st.session_state:
#     st.session_state.total_tokens = 0


# def login(username: str, password: str) -> bool:
#     """Login user"""
#     try:
#         response = requests.post(
#             f"{API_URL}/auth/login",
#             json={"username": username, "password": password}
#         )
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.token = data["access_token"]
#             st.session_state.username = username
#             return True
#         return False
#     except Exception as e:
#         st.error(f"🔌 Connection error: {str(e)}")
#         return False


# def register(username: str, email: str, password: str) -> bool:
#     """Register new user"""
#     try:
#         response = requests.post(
#             f"{API_URL}/auth/register",
#             json={"username": username, "email": email, "password": password}
#         )
#         return response.status_code == 201
#     except Exception as e:
#         st.error(f"🔌 Connection error: {str(e)}")
#         return False


# def send_message(message: str, provider: str, model: str, temperature: float, max_tokens: int) -> Optional[dict]:
#     """Send message to LLM"""
#     try:
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         response = requests.post(
#             f"{API_URL}/chat/",
#             headers=headers,
#             json={
#                 "message": message,
#                 "provider": provider,
#                 "model": model,
#                 "temperature": temperature,
#                 "max_tokens": max_tokens
#             }
#         )
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except Exception as e:
#         st.error(f"⚠️ Error: {str(e)}")
#         return None


# def get_history() -> list:
#     """Get conversation history"""
#     try:
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         response = requests.get(f"{API_URL}/chat/history?limit=50", headers=headers)
#         if response.status_code == 200:
#             return response.json()["conversations"]
#         return []
#     except:
#         return []


# def create_cost_chart():
#     """Create advanced cost visualization"""
#     if not st.session_state.chat_history:
#         return None
    
#     costs = [msg.get('cost', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
#     if not costs:
#         return None
        
#     timestamps = list(range(1, len(costs) + 1))
    
#     fig = go.Figure()
    
#     # Main line
#     fig.add_trace(go.Scatter(
#         x=timestamps,
#         y=costs,
#         mode='lines+markers',
#         name='Cost per message',
#         line=dict(color='#667eea', width=3, shape='spline'),
#         marker=dict(
#             size=10,
#             color='#764ba2',
#             line=dict(color='white', width=2)
#         ),
#         fill='tozeroy',
#         fillcolor='rgba(102, 126, 234, 0.2)'
#     ))
    
#     # Cumulative cost
#     cumulative = [sum(costs[:i+1]) for i in range(len(costs))]
#     fig.add_trace(go.Scatter(
#         x=timestamps,
#         y=cumulative,
#         mode='lines',
#         name='Cumulative cost',
#         line=dict(color='#f093fb', width=2, dash='dash'),
#         yaxis='y2'
#     ))
    
#     fig.update_layout(
#         title={
#             'text': '💰 Cost Analytics',
#             'font': {'size': 20, 'color': 'white', 'family': 'Inter'}
#         },
#         xaxis_title='Message Number',
#         yaxis_title='Cost per Message ($)',
#         yaxis2=dict(
#             title='Cumulative Cost ($)',
#             overlaying='y',
#             side='right'
#         ),
#         template='plotly_dark',
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=350,
#         margin=dict(l=20, r=20, t=50, b=20),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1
#         ),
#         hovermode='x unified'
#     )
    
#     return fig


# def create_token_distribution():
#     """Create token usage distribution"""
#     if not st.session_state.chat_history:
#         return None
        
#     tokens = [msg.get('tokens', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
#     if not tokens:
#         return None
        
#     fig = go.Figure(data=[go.Bar(
#         x=list(range(1, len(tokens) + 1)),
#         y=tokens,
#         marker=dict(
#             color=tokens,
#             colorscale='Viridis',
#             showscale=True,
#             colorbar=dict(title="Tokens")
#         )
#     )])
    
#     fig.update_layout(
#         title={
#             'text': '🎯 Token Usage Distribution',
#             'font': {'size': 20, 'color': 'white', 'family': 'Inter'}
#         },
#         xaxis_title='Message Number',
#         yaxis_title='Tokens Used',
#         template='plotly_dark',
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=300,
#         margin=dict(l=20, r=20, t=50, b=20)
#     )
    
#     return fig


# # Main UI
# st.markdown("""
#     <div style='text-align: center; padding: 30px 20px;'>
#         <h1 style='font-size: 4rem; margin-bottom: 10px; background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%); 
#                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
#             🤖 AI Assistant Pro
#         </h1>
#         <p style='font-size: 1.3rem; color: rgba(255,255,255,0.85); margin-top: 10px; font-weight: 300;'>
#             Your Premium Multi-LLM Intelligence Platform
#         </p>
#         <div style='margin-top: 20px;'>
#             <span class='badge'>✨ Powered by GPT-4 & Claude</span>
#             <span class='badge'>🚀 Real-time Analytics</span>
#             <span class='badge'>🔒 Secure & Private</span>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # Authentication UI
# if not st.session_state.token:
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])
        
#         with tab1:
#             st.markdown("<div class='card'>", unsafe_allow_html=True)
#             st.markdown("### 👋 Welcome Back!")
#             st.markdown("<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Sign in to continue your AI journey</p>", unsafe_allow_html=True)
            
#             with st.form("login_form"):
#                 login_username = st.text_input("👤 Username", placeholder="Enter your username")
#                 login_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
#                 col_a, col_b, col_c = st.columns([1, 2, 1])
#                 with col_b:
#                     submit_login = st.form_submit_button("🚀 Sign In", use_container_width=True)
                
#                 if submit_login:
#                     if login_username and login_password:
#                         with st.spinner("🔄 Authenticating..."):
#                             if login(login_username, login_password):
#                                 st.success("✅ Welcome back! Redirecting...")
#                                 st.balloons()
#                                 time.sleep(1)
#                                 st.rerun()
#                             else:
#                                 st.error("❌ Invalid credentials. Please try again.")
#                     else:
#                         st.warning("⚠️ Please fill in all fields")
            
#             st.markdown("</div>", unsafe_allow_html=True)
        
#         with tab2:
#             st.markdown("<div class='card'>", unsafe_allow_html=True)
#             st.markdown("### ✨ Join AI Assistant Pro")
#             st.markdown("<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Create your account in seconds</p>", unsafe_allow_html=True)
            
#             with st.form("register_form"):
#                 reg_username = st.text_input("👤 Username", placeholder="Choose a unique username")
#                 reg_email = st.text_input("📧 Email", placeholder="your.email@example.com")
#                 reg_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                
#                 col_a, col_b, col_c = st.columns([1, 2, 1])
#                 with col_b:
#                     submit_register = st.form_submit_button("✨ Create Account", use_container_width=True)
                
#                 if submit_register:
#                     if reg_username and reg_email and reg_password:
#                         with st.spinner("🔄 Creating your account..."):
#                             if register(reg_username, reg_email, reg_password):
#                                 st.success("✅ Account created successfully! Please sign in.")
#                                 st.balloons()
#                             else:
#                                 st.error("❌ Registration failed. Username or email may already exist.")
#                     else:
#                         st.warning("⚠️ Please fill in all fields")
            
#             st.markdown("</div>", unsafe_allow_html=True)

# else:
#     # Sidebar for authenticated users
#     with st.sidebar:
#         st.markdown(f"""
#             <div class='card' style='text-align: center; margin-bottom: 25px;'>
#                 <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
#                             width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 15px;
#                             display: flex; align-items: center; justify-content: center;
#                             font-size: 36px; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);'>
#                     👤
#                 </div>
#                 <h2 style='color: white; margin: 0; font-size: 24px;'>{st.session_state.username}</h2>
#                 <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin-top: 5px;'>Premium Member</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("🚪 Sign Out", use_container_width=True):
#             st.session_state.token = None
#             st.session_state.username = None
#             st.session_state.chat_history = []
#             st.session_state.total_cost = 0.0
#             st.session_state.total_tokens = 0
#             st.rerun()
        
#         st.markdown("---")
        
#         # Statistics with cards
#         st.markdown("### 📊 Session Analytics")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric(
#                 "💬 Messages",
#                 len([m for m in st.session_state.chat_history if m['role'] == 'user']),
#                 delta=None
#             )
#         with col2:
#             st.metric(
#                 "💰 Cost",
#                 f"${st.session_state.total_cost:.4f}",
#                 delta=None
#             )
        
#         st.metric(
#             "🎯 Tokens",
#             f"{st.session_state.total_tokens:,}",
#             delta=None
#         )
        
#         st.markdown("---")
        
#         # LLM Settings
#         st.markdown("### ⚙️ Model Configuration")
        
#         provider = st.selectbox(
#             "🤖 AI Provider",
#             ["openai", "anthropic"],
#             help="Select your preferred AI provider"
#         )
        
#         if provider == "openai":
#             model_options = {
#                 "GPT-3.5 Turbo ⚡": "gpt-3.5-turbo",
#                 "GPT-4 🧠": "gpt-4",
#                 "GPT-4 Turbo 🚀": "gpt-4-turbo"
#             }
#         else:
#             model_options = {
#                 "Claude 3 Haiku ⚡": "claude-3-haiku-20240307",
#                 "Claude 3 Sonnet 🎭": "claude-3-sonnet-20240229",
#                 "Claude 3 Opus 👑": "claude-3-opus-20240229"
#             }
        
#         model_display = st.selectbox("🎯 Model", list(model_options.keys()))
#         model = model_options[model_display]
        
#         temperature = st.slider(
#             "🌡️ Temperature",
#             0.0, 2.0, 0.7, 0.1,
#             help="Higher values = more creative | Lower values = more focused"
#         )
        
#         max_tokens = st.slider(
#             "📝 Max Tokens",
#             100, 4000, 1000, 100,
#             help="Maximum length of the AI response"
#         )
        
#         st.markdown("---")
        
#         # History controls
#         st.markdown("### 📚 Conversation History")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("📥 Load", use_container_width=True):
#                 with st.spinner("🔄 Loading history..."):
#                     history = get_history()
#                     if history:
#                         st.session_state.chat_history = []
#                         for h in reversed(history):
#                             st.session_state.chat_history.append({
#                                 "role": "user",
#                                 "content": h["message"],
#                                 "timestamp": h["created_at"]
#                             })
#                             st.session_state.chat_history.append({
#                                 "role": "assistant",
#                                 "content": h["response"],
#                                 "provider": h["provider"],
#                                 "model": h["model"],
#                                 "cost": h["cost"],
#                                 "tokens": h["tokens_used"]
#                             })
#                         st.success("✅ History loaded successfully!")
#                         time.sleep(0.5)
#                         st.rerun()
        
#         with col2:
#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.session_state.total_cost = 0.0
#                 st.session_state.total_tokens = 0
#                 st.rerun()
        
#         # Visualizations
#         if len([m for m in st.session_state.chat_history if m['role'] == 'assistant']) > 0:
#             st.markdown("---")
#             st.markdown("### 📈 Analytics Dashboard")
            
#             # Cost chart
#             fig = create_cost_chart()
#             if fig:
#                 st.plotly_chart(fig, use_container_width=True)
            
#             # Token distribution
#             fig2 = create_token_distribution()
#             if fig2:
#                 st.plotly_chart(fig2, use_container_width=True)
    
#     # Main chat area
#     st.markdown("### 💬 AI Conversation")
    
#     # Chat container
#     chat_container = st.container()
    
#     with chat_container:
#         for idx, msg in enumerate(st.session_state.chat_history):
#             with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
#                 st.markdown(msg["content"])
                
#                 if msg["role"] == "assistant" and "cost" in msg:
#                     st.markdown(f"""
#                         <div class='card' style='margin-top: 15px; padding: 12px;'>
#                             <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 13px;'>
#                                 <div>
#                                     <span style='color: rgba(255,255,255,0.6);'>Provider:</span>
#                                     <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('provider', 'N/A').upper()}</span>
#                                 </div>
#                                 <div>
#                                     <span style='color: rgba(255,255,255,0.6);'>Model:</span>
#                                     <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('model', 'N/A')}</span>
#                                 </div>
#                                 <div>
#                                     <span style='color: rgba(255,255,255,0.6);'>Tokens:</span>
#                                     <span style='color: white; font-weight: 600; margin-left: 5px;'>{msg.get('tokens', 0):,}</span>
#                                 </div>
#                                 <div>
#                                     <span style='color: rgba(255,255,255,0.6);'>Cost:</span>

# # # Professional Streamlit UI for AI Assistant with Modern Design
# # # """)
                    
                    
                    
                
                
                
                
                
                    
                    
# import streamlit as st
# import requests
# from datetime import datetime
# import plotly.graph_objects as go
# import plotly.express as px
# from typing import Optional

# # Configuration
# # API_URL = "http://localhost:8000"
# API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# # Custom CSS for professional look
# st.markdown("""
# <style>
#     /* Main container */
#     .main {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     }
    
#     /* Sidebar styling */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
#     }
    
#     [data-testid="stSidebar"] .element-container {
#         color: white;
#     }
    
#     /* Chat messages */
#     .stChatMessage {
#         background: rgba(255, 255, 255, 0.95);
#         border-radius: 15px;
#         padding: 20px;
#         margin: 10px 0;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         backdrop-filter: blur(10px);
#     }
    
#     /* Headers */
#     h1, h2, h3 {
#         color: white !important;
#         font-weight: 700;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
#     }
    
#     /* Buttons */
#     .stButton > button {
#         width: 100%;
#         border-radius: 10px;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         font-weight: 600;
#         border: none;
#         padding: 12px;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
#     }
    
#     /* Input fields */
#     .stTextInput > div > div > input {
#         border-radius: 10px;
#         border: 2px solid #667eea;
#         padding: 12px;
#     }
    
#     /* Metrics */
#     [data-testid="stMetricValue"] {
#         font-size: 28px;
#         font-weight: 700;
#         color: #667eea;
#     }
    
#     /* Success/Error messages */
#     .stSuccess {
#         background: rgba(76, 175, 80, 0.1);
#         border-left: 5px solid #4CAF50;
#         border-radius: 10px;
#     }
    
#     .stError {
#         background: rgba(244, 67, 54, 0.1);
#         border-left: 5px solid #F44336;
#         border-radius: 10px;
#     }
    
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 10px;
#         padding: 5px;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px;
#         color: white;
#         font-weight: 600;
#     }
    
#     /* Chat input */
#     .stChatInput > div > div > textarea {
#         border-radius: 20px;
#         border: 2px solid #667eea;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Page config
# st.set_page_config(
#     page_title="AI Assistant Pro",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize session state
# if 'token' not in st.session_state:
#     st.session_state.token = None
# if 'username' not in st.session_state:
#     st.session_state.username = None
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'total_cost' not in st.session_state:
#     st.session_state.total_cost = 0.0
# if 'total_tokens' not in st.session_state:
#     st.session_state.total_tokens = 0


# def show_typing_animation():
#     """Show typing animation"""
#     return st.markdown("""
#         <div style="display: flex; align-items: center; gap: 5px;">
#             <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.32s;"></div>
#             <div style="width: 8px; height: 8px; background: #764ba2; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.16s;"></div>
#             <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both;"></div>
#         </div>
#         <style>
#         @keyframes bounce {
#             0%, 80%, 100% { transform: scale(0); }
#             40% { transform: scale(1); }
#         }
#         </style>
#     """, unsafe_allow_html=True)


# def login(username: str, password: str) -> bool:
#     """Login user"""
#     try:
#         response = requests.post(
#             f"{API_URL}/auth/login",
#             json={"username": username, "password": password}
#         )
#         if response.status_code == 200:
#             data = response.json()
#             st.session_state.token = data["access_token"]
#             st.session_state.username = username
#             return True
#         return False
#     except Exception as e:
#         st.error(f"Connection error: {str(e)}")
#         return False


# def register(username: str, email: str, password: str) -> bool:
#     """Register new user"""
#     try:
#         response = requests.post(
#             f"{API_URL}/auth/register",
#             json={"username": username, "email": email, "password": password}
#         )
#         return response.status_code == 201
#     except Exception as e:
#         st.error(f"Connection error: {str(e)}")
#         return False


# def send_message(message: str, provider: str, model: str, temperature: float, max_tokens: int) -> Optional[dict]:
#     """Send message to LLM"""
#     try:
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         response = requests.post(
#             f"{API_URL}/chat/",
#             headers=headers,
#             json={
#                 "message": message,
#                 "provider": provider,
#                 "model": model,
#                 "temperature": temperature,
#                 "max_tokens": max_tokens
#             }
#         )
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return None


# def get_history() -> list:
#     """Get conversation history"""
#     try:
#         headers = {"Authorization": f"Bearer {st.session_state.token}"}
#         response = requests.get(f"{API_URL}/chat/history?limit=50", headers=headers)
#         if response.status_code == 200:
#             return response.json()["conversations"]
#         return []
#     except:
#         return []


# def create_cost_chart():
#     """Create cost visualization"""
#     if not st.session_state.chat_history:
#         return None
    
#     costs = [msg.get('cost', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
#     timestamps = list(range(1, len(costs) + 1))
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=timestamps,
#         y=costs,
#         mode='lines+markers',
#         name='Cost per message',
#         line=dict(color='#667eea', width=3),
#         marker=dict(size=8, color='#764ba2')
#     ))
    
#     fig.update_layout(
#         title='💰 Cost Tracking',
#         xaxis_title='Message Number',
#         yaxis_title='Cost ($)',
#         template='plotly_dark',
#         height=300,
#         margin=dict(l=0, r=0, t=40, b=0)
#     )
    
#     return fig


# # Main UI
# st.markdown("""
#     <div style='text-align: center; padding: 20px;'>
#         <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🤖 AI Assistant Pro</h1>
#         <p style='font-size: 1.2rem; color: rgba(255,255,255,0.8); margin-top: 10px;'>
#             Your Intelligent Multi-LLM Companion
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Authentication UI
# if not st.session_state.token:
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         st.markdown("<br><br>", unsafe_allow_html=True)
        
#         tab1, tab2 = st.tabs(["🔐 Login", "✨ Register"])
        
#         with tab1:
#             st.markdown("### Welcome Back!")
#             with st.form("login_form"):
#                 login_username = st.text_input("👤 Username", placeholder="Enter your username")
#                 login_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
#                 submit_login = st.form_submit_button("🚀 Login", use_container_width=True)
                
#                 if submit_login:
#                     if login_username and login_password:
#                         with st.spinner("Authenticating..."):
#                             if login(login_username, login_password):
#                                 st.success("✅ Login successful!")
#                                 st.balloons()
#                                 st.rerun()
#                             else:
#                                 st.error("❌ Invalid credentials")
#                     else:
#                         st.warning("⚠️ Please fill all fields")
        
#         with tab2:
#             st.markdown("### Create Account")
#             with st.form("register_form"):
#                 reg_username = st.text_input("👤 Username", placeholder="Choose a username")
#                 reg_email = st.text_input("📧 Email", placeholder="your.email@example.com")
#                 reg_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
#                 submit_register = st.form_submit_button("✨ Create Account", use_container_width=True)
                
#                 if submit_register:
#                     if reg_username and reg_email and reg_password:
#                         with st.spinner("Creating account..."):
#                             if register(reg_username, reg_email, reg_password):
#                                 st.success("✅ Registration successful! Please login.")
#                                 st.balloons()
#                             else:
#                                 st.error("❌ Registration failed. Username or email may exist.")
#                     else:
#                         st.warning("⚠️ Please fill all fields")

# else:
#     # Sidebar for authenticated users
#     with st.sidebar:
#         st.markdown(f"""
#             <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
#                         padding: 20px; border-radius: 15px; margin-bottom: 20px;
#                         box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
#                 <h2 style='color: white; text-align: center; margin: 0;'>👤 {st.session_state.username}</h2>
#             </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("🚪 Logout", use_container_width=True):
#             st.session_state.token = None
#             st.session_state.username = None
#             st.session_state.chat_history = []
#             st.session_state.total_cost = 0.0
#             st.session_state.total_tokens = 0
#             st.rerun()
        
#         st.markdown("---")
        
#         # Statistics
#         st.markdown("### 📊 Session Stats")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("💬 Messages", len([m for m in st.session_state.chat_history if m['role'] == 'user']))
#         with col2:
#             st.metric("💰 Total Cost", f"${st.session_state.total_cost:.4f}")
        
#         st.metric("🎯 Tokens Used", f"{st.session_state.total_tokens:,}")
        
#         st.markdown("---")
        
#         # LLM Settings
#         st.markdown("### ⚙️ Model Settings")
        
#         provider = st.selectbox(
#             "🤖 Provider",
#             ["openai", "anthropic"],
#             help="Choose your AI provider"
#         )
        
#         if provider == "openai":
#             model_options = {
#                 "GPT-3.5 Turbo": "gpt-3.5-turbo",
#                 "GPT-4": "gpt-4",
#                 "GPT-4 Turbo": "gpt-4-turbo"
#             }
#         else:
#             model_options = {
#                 "Claude 3 Haiku": "claude-3-haiku-20240307",
#                 "Claude 3 Sonnet": "claude-3-sonnet-20240229",
#                 "Claude 3 Opus": "claude-3-opus-20240229"
#             }
        
#         model_display = st.selectbox("🎯 Model", list(model_options.keys()))
#         model = model_options[model_display]
        
#         temperature = st.slider(
#             "🌡️ Temperature",
#             0.0, 2.0, 0.7, 0.1,
#             help="Higher = more creative, Lower = more focused"
#         )
        
#         max_tokens = st.slider(
#             "📝 Max Tokens",
#             100, 4000, 1000, 100,
#             help="Maximum length of response"
#         )
        
#         st.markdown("---")
        
#         # History controls
#         st.markdown("### 📚 History")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("📜 Load", use_container_width=True):
#                 with st.spinner("Loading..."):
#                     history = get_history()
#                     if history:
#                         st.session_state.chat_history = []
#                         for h in reversed(history):
#                             st.session_state.chat_history.append({
#                                 "role": "user", 
#                                 "content": h["message"],
#                                 "timestamp": h["created_at"]
#                             })
#                             st.session_state.chat_history.append({
#                                 "role": "assistant",
#                                 "content": h["response"],
#                                 "provider": h["provider"],
#                                 "model": h["model"],
#                                 "cost": h["cost"],
#                                 "tokens": h["tokens_used"]
#                             })
#                         st.success("✅ History loaded!")
#                         st.rerun()
        
#         with col2:
#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.session_state.total_cost = 0.0
#                 st.session_state.total_tokens = 0
#                 st.rerun()
        
#         # Cost visualization
#         if len([m for m in st.session_state.chat_history if m['role'] == 'assistant']) > 0:
#             st.markdown("---")
#             fig = create_cost_chart()
#             if fig:
#                 st.plotly_chart(fig, use_container_width=True)
    
#     # Main chat area
#     st.markdown("### 💬 Conversation")
    
#     # Chat container
#     chat_container = st.container()
    
#     with chat_container:
#         for idx, msg in enumerate(st.session_state.chat_history):
#             with st.chat_message(msg["role"]):
#                 st.markdown(msg["content"])
                
#                 if msg["role"] == "assistant" and "cost" in msg:
#                     st.markdown(f"""
#                         <div style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
#                                     padding: 10px; border-radius: 10px; margin-top: 10px;'>
#                             <small>
#                                 <b>Provider:</b> {msg.get('provider', 'N/A').upper()} | 
#                                 <b>Model:</b> {msg.get('model', 'N/A')} | 
#                                 <b>Tokens:</b> {msg.get('tokens', 0):,} | 
#                                 <b>Cost:</b> ${msg.get('cost', 0):.6f}
#                             </small>
#                         </div>
#                     """, unsafe_allow_html=True)
    
#     # Chat input
#     if prompt := st.chat_input("💭 Type your message here...", key="chat_input"):
#         # Add user message
#         st.session_state.chat_history.append({
#             "role": "user",
#             "content": prompt,
#             "timestamp": datetime.now().isoformat()
#         })
        
#         with st.chat_message("user"):
#             st.markdown(prompt)
        
#         # Get AI response
#         with st.chat_message("assistant"):
#             with st.spinner("🤔 Thinking..."):
#                 response = send_message(prompt, provider, model, temperature, max_tokens)
                
#                 if response:
#                     st.markdown(response["response"])
                    
#                     # Update statistics
#                     st.session_state.total_cost += response["cost"]
#                     st.session_state.total_tokens += response["tokens_used"]
                    
#                     st.markdown(f"""
#                         <div style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
#                                     padding: 10px; border-radius: 10px; margin-top: 10px;'>
#                             <small>
#                                 <b>Provider:</b> {response['provider'].upper()} | 
#                                 <b>Model:</b> {response['model']} | 
#                                 <b>Tokens:</b> {response['tokens_used']:,} | 
#                                 <b>Cost:</b> ${response['cost']:.6f}
#                             </small>
#                         </div>
#                     """, unsafe_allow_html=True)
                    
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": response["response"],
#                         "provider": response["provider"],
#                         "model": response["model"],
#                         "tokens": response["tokens_used"],
#                         "cost": response["cost"]
#                     })
                    
#                     st.rerun()
#                 else:
#                     st.error("❌ Failed to get response. Please try again.")




