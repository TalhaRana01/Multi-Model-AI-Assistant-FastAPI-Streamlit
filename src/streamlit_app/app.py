"""
Professional Streamlit UI for AI Assistant with Modern Design
"""
import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional

# Configuration
# API_URL = "http://localhost:8000"
API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 12px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1);
        border-left: 5px solid #4CAF50;
        border-radius: 10px;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.1);
        border-left: 5px solid #F44336;
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: white;
        font-weight: 600;
    }
    
    /* Chat input */
    .stChatInput > div > div > textarea {
        border-radius: 20px;
        border: 2px solid #667eea;
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


def show_typing_animation():
    """Show typing animation"""
    return st.markdown("""
        <div style="display: flex; align-items: center; gap: 5px;">
            <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.32s;"></div>
            <div style="width: 8px; height: 8px; background: #764ba2; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; animation-delay: -0.16s;"></div>
            <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both;"></div>
        </div>
        <style>
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)


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
        st.error(f"Connection error: {str(e)}")
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
        st.error(f"Connection error: {str(e)}")
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
        st.error(f"Error: {str(e)}")
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
    """Create cost visualization"""
    if not st.session_state.chat_history:
        return None
    
    costs = [msg.get('cost', 0) for msg in st.session_state.chat_history if msg['role'] == 'assistant']
    timestamps = list(range(1, len(costs) + 1))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=costs,
        mode='lines+markers',
        name='Cost per message',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2')
    ))
    
    fig.update_layout(
        title='💰 Cost Tracking',
        xaxis_title='Message Number',
        yaxis_title='Cost ($)',
        template='plotly_dark',
        height=300,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


# Main UI
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🤖 AI Assistant Pro</h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.8); margin-top: 10px;'>
            Your Intelligent Multi-LLM Companion
        </p>
    </div>
""", unsafe_allow_html=True)

# Authentication UI
if not st.session_state.token:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Register"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            with st.form("login_form"):
                login_username = st.text_input("👤 Username", placeholder="Enter your username")
                login_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit_login:
                    if login_username and login_password:
                        with st.spinner("Authenticating..."):
                            if login(login_username, login_password):
                                st.success("✅ Login successful!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials")
                    else:
                        st.warning("⚠️ Please fill all fields")
        
        with tab2:
            st.markdown("### Create Account")
            with st.form("register_form"):
                reg_username = st.text_input("👤 Username", placeholder="Choose a username")
                reg_email = st.text_input("📧 Email", placeholder="your.email@example.com")
                reg_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                submit_register = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if submit_register:
                    if reg_username and reg_email and reg_password:
                        with st.spinner("Creating account..."):
                            if register(reg_username, reg_email, reg_password):
                                st.success("✅ Registration successful! Please login.")
                                st.balloons()
                            else:
                                st.error("❌ Registration failed. Username or email may exist.")
                    else:
                        st.warning("⚠️ Please fill all fields")

else:
    # Sidebar for authenticated users
    with st.sidebar:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; margin-bottom: 20px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <h2 style='color: white; text-align: center; margin: 0;'>👤 {st.session_state.username}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.chat_history = []
            st.session_state.total_cost = 0.0
            st.session_state.total_tokens = 0
            st.rerun()
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💬 Messages", len([m for m in st.session_state.chat_history if m['role'] == 'user']))
        with col2:
            st.metric("💰 Total Cost", f"${st.session_state.total_cost:.4f}")
        
        st.metric("🎯 Tokens Used", f"{st.session_state.total_tokens:,}")
        
        st.markdown("---")
        
        # LLM Settings
        st.markdown("### ⚙️ Model Settings")
        
        provider = st.selectbox(
            "🤖 Provider",
            ["openai", "anthropic"],
            help="Choose your AI provider"
        )
        
        if provider == "openai":
            model_options = {
                "GPT-3.5 Turbo": "gpt-3.5-turbo",
                "GPT-4": "gpt-4",
                "GPT-4 Turbo": "gpt-4-turbo"
            }
        else:
            model_options = {
                "Claude 3 Haiku": "claude-3-haiku-20240307",
                "Claude 3 Sonnet": "claude-3-sonnet-20240229",
                "Claude 3 Opus": "claude-3-opus-20240229"
            }
        
        model_display = st.selectbox("🎯 Model", list(model_options.keys()))
        model = model_options[model_display]
        
        temperature = st.slider(
            "🌡️ Temperature",
            0.0, 2.0, 0.7, 0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        max_tokens = st.slider(
            "📝 Max Tokens",
            100, 4000, 1000, 100,
            help="Maximum length of response"
        )
        
        st.markdown("---")
        
        # History controls
        st.markdown("### 📚 History")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📜 Load", use_container_width=True):
                with st.spinner("Loading..."):
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
                        st.success("✅ History loaded!")
                        st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.total_cost = 0.0
                st.session_state.total_tokens = 0
                st.rerun()
        
        # Cost visualization
        if len([m for m in st.session_state.chat_history if m['role'] == 'assistant']) > 0:
            st.markdown("---")
            fig = create_cost_chart()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Main chat area
    st.markdown("### 💬 Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for idx, msg in enumerate(st.session_state.chat_history):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                if msg["role"] == "assistant" and "cost" in msg:
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
                                    padding: 10px; border-radius: 10px; margin-top: 10px;'>
                            <small>
                                <b>Provider:</b> {msg.get('provider', 'N/A').upper()} | 
                                <b>Model:</b> {msg.get('model', 'N/A')} | 
                                <b>Tokens:</b> {msg.get('tokens', 0):,} | 
                                <b>Cost:</b> ${msg.get('cost', 0):.6f}
                            </small>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("💭 Type your message here...", key="chat_input"):
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = send_message(prompt, provider, model, temperature, max_tokens)
                
                if response:
                    st.markdown(response["response"])
                    
                    # Update statistics
                    st.session_state.total_cost += response["cost"]
                    st.session_state.total_tokens += response["tokens_used"]
                    
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
                                    padding: 10px; border-radius: 10px; margin-top: 10px;'>
                            <small>
                                <b>Provider:</b> {response['provider'].upper()} | 
                                <b>Model:</b> {response['model']} | 
                                <b>Tokens:</b> {response['tokens_used']:,} | 
                                <b>Cost:</b> ${response['cost']:.6f}
                            </small>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["response"],
                        "provider": response["provider"],
                        "model": response["model"],
                        "tokens": response["tokens_used"],
                        "cost": response["cost"]
                    })
                    
                    st.rerun()
                else:
                    st.error("❌ Failed to get response. Please try again.")




# """
# Streamlit UI for AI Assistant
# """
# import streamlit as st
# import requests
# from datetime import datetime
# import pandas as pd

# # Configuration
# # API_URL = "http://localhost:8000"
# API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# # Page config
# st.set_page_config(
#     page_title="AI Assistant",
#     page_icon="🤖",
#     layout="wide"
# )

# # Initialize session state
# if 'token' not in st.session_state:
#     st.session_state.token = None
# if 'username' not in st.session_state:
#     st.session_state.username = None
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []


# def login(username: str, password: str):
#     """Login user"""
#     response = requests.post(
#         f"{API_URL}/auth/login",
#         json={"username": username, "password": password}
#     )
#     if response.status_code == 200:
#         data = response.json()
#         st.session_state.token = data["access_token"]
#         st.session_state.username = username
#         return True
#     return False


# def register(username: str, email: str, password: str):
#     """Register new user"""
#     response = requests.post(
#         f"{API_URL}/auth/register",
#         json={"username": username, "email": email, "password": password}
#     )
#     return response.status_code == 201


# def send_message(message: str, provider: str, model: str, temperature: float, max_tokens: int):
#     """Send message to LLM"""
#     headers = {"Authorization": f"Bearer {st.session_state.token}"}
#     response = requests.post(
#         f"{API_URL}/chat/",
#         headers=headers,
#         json={
#             "message": message,
#             "provider": provider,
#             "model": model,
#             "temperature": temperature,
#             "max_tokens": max_tokens
#         }
#     )
#     if response.status_code == 200:
#         return response.json()
#     return None


# def get_history():
#     """Get conversation history"""
#     headers = {"Authorization": f"Bearer {st.session_state.token}"}
#     response = requests.get(f"{API_URL}/chat/history?limit=50", headers=headers)
#     if response.status_code == 200:
#         return response.json()["conversations"]
#     return []


# # UI
# st.title("🤖 AI Assistant")

# # Authentication
# if not st.session_state.token:
#     tab1, tab2 = st.tabs(["Login", "Register"])
    
#     with tab1:
#         st.subheader("Login")
#         login_username = st.text_input("Username", key="login_user")
#         login_password = st.text_input("Password", type="password", key="login_pass")
        
#         if st.button("Login"):
#             if login(login_username, login_password):
#                 st.success("Logged in successfully!")
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials")
    
#     with tab2:
#         st.subheader("Register")
#         reg_username = st.text_input("Username", key="reg_user")
#         reg_email = st.text_input("Email", key="reg_email")
#         reg_password = st.text_input("Password", type="password", key="reg_pass")
        
#         if st.button("Register"):
#             if register(reg_username, reg_email, reg_password):
#                 st.success("Registration successful! Please login.")
#             else:
#                 st.error("Registration failed. Username or email may already exist.")

# else:
#     # Sidebar
#     with st.sidebar:
#         st.success(f"Logged in as: {st.session_state.username}")
        
#         if st.button("Logout"):
#             st.session_state.token = None
#             st.session_state.username = None
#             st.session_state.chat_history = []
#             st.rerun()
        
#         st.divider()
        
#         # LLM Settings
#         st.subheader("⚙️ Settings")
#         provider = st.selectbox("Provider", ["openai", "anthropic"])
        
#         if provider == "openai":
#             model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
#         else:
#             model = st.selectbox("Model", [
#                 "claude-3-haiku-20240307",
#                 "claude-3-sonnet-20240229",
#                 "claude-3-opus-20240229"
#             ])
        
#         temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
#         max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
        
#         st.divider()
        
#         # History
#         if st.button("📜 Load History"):
#             history = get_history()
#             st.session_state.chat_history = [
#                 {"role": "user", "content": h["message"], "timestamp": h["created_at"]}
#                 for h in history
#             ] + [
#                 {"role": "assistant", "content": h["response"], 
#                  "provider": h["provider"], "cost": h["cost"], "tokens": h["tokens_used"]}
#                 for h in history
#             ]
    
#     # Main chat area
#     st.subheader("💬 Chat")
    
#     # Display chat history
#     for msg in st.session_state.chat_history:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])
#             if msg["role"] == "assistant" and "cost" in msg:
#                 st.caption(f"Provider: {msg.get('provider', 'N/A')} | "
#                           f"Tokens: {msg.get('tokens', 0)} | "
#                           f"Cost: ${msg.get('cost', 0):.6f}")
    
#     # Chat input
#     if prompt := st.chat_input("Type your message..."):
#         # Add user message
#         st.session_state.chat_history.append({"role": "user", "content": prompt})
        
#         with st.chat_message("user"):
#             st.write(prompt)
        
#         # Get AI response
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = send_message(prompt, provider, model, temperature, max_tokens)
                
#                 if response:
#                     st.write(response["response"])
#                     st.caption(f"Provider: {response['provider']} | "
#                               f"Tokens: {response['tokens_used']} | "
#                               f"Cost: ${response['cost']:.6f}")
                    
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": response["response"],
#                         "provider": response["provider"],
#                         "tokens": response["tokens_used"],
#                         "cost": response["cost"]
#                     })
#                 else:
#                     st.error("Failed to get response")