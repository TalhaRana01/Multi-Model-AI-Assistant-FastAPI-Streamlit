"""
Streamlit UI for AI Assistant
"""
import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configuration
# API_URL = "http://localhost:8000"
API_URL = "https://multi-model-ai-assistant-fastapi-streamlit-production.up.railway.app/"

# Page config
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def login(username: str, password: str):
    """Login user"""
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


def register(username: str, email: str, password: str):
    """Register new user"""
    response = requests.post(
        f"{API_URL}/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    return response.status_code == 201


def send_message(message: str, provider: str, model: str, temperature: float, max_tokens: int):
    """Send message to LLM"""
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


def get_history():
    """Get conversation history"""
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/chat/history?limit=50", headers=headers)
    if response.status_code == 200:
        return response.json()["conversations"]
    return []


# UI
st.title("🤖 AI Assistant")

# Authentication
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if login(login_username, login_password):
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        st.subheader("Register")
        reg_username = st.text_input("Username", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        
        if st.button("Register"):
            if register(reg_username, reg_email, reg_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Registration failed. Username or email may already exist.")

else:
    # Sidebar
    with st.sidebar:
        st.success(f"Logged in as: {st.session_state.username}")
        
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.divider()
        
        # LLM Settings
        st.subheader("⚙️ Settings")
        provider = st.selectbox("Provider", ["openai", "anthropic"])
        
        if provider == "openai":
            model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        else:
            model = st.selectbox("Model", [
                "claude-3-haiku-20240307",
                "claude-3-sonnet-20240229",
                "claude-3-opus-20240229"
            ])
        
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
        
        st.divider()
        
        # History
        if st.button("📜 Load History"):
            history = get_history()
            st.session_state.chat_history = [
                {"role": "user", "content": h["message"], "timestamp": h["created_at"]}
                for h in history
            ] + [
                {"role": "assistant", "content": h["response"], 
                 "provider": h["provider"], "cost": h["cost"], "tokens": h["tokens_used"]}
                for h in history
            ]
    
    # Main chat area
    st.subheader("💬 Chat")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "cost" in msg:
                st.caption(f"Provider: {msg.get('provider', 'N/A')} | "
                          f"Tokens: {msg.get('tokens', 0)} | "
                          f"Cost: ${msg.get('cost', 0):.6f}")
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt, provider, model, temperature, max_tokens)
                
                if response:
                    st.write(response["response"])
                    st.caption(f"Provider: {response['provider']} | "
                              f"Tokens: {response['tokens_used']} | "
                              f"Cost: ${response['cost']:.6f}")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["response"],
                        "provider": response["provider"],
                        "tokens": response["tokens_used"],
                        "cost": response["cost"]
                    })
                else:
                    st.error("Failed to get response")