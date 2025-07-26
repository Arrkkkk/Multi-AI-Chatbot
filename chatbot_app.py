import streamlit as st
import os
from datetime import datetime

# Add import for Google GenAI
try:
    from google import genai
except ImportError:
    genai = None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
try:
    import anthropic
except ImportError:
    anthropic = None
try:
    import groq
except ImportError:
    groq = None

# Initialize session state variables at the very top
for k, v in {
    "provider": None,
    "api_key": "",
    "chat_history": [],
    "show_settings": False,
    "show_api_success": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Supported AI providers
AI_PROVIDERS = ["Claude", "OpenAI", "Gemini", "Groq"]

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(205, 133, 63, 0.3);
    }



    .user-message {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        color: white;
        padding: 1rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 6px 20px rgba(205, 133, 63, 0.25);
    }

    .ai-message {
        background: linear-gradient(135deg, #FFF8DC 0%, #F5DEB3 100%);
        color: #8B4513;
        padding: 1rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border: 1px solid #DEB887;
        box-shadow: 0 6px 20px rgba(205, 133, 63, 0.15);
    }

    .provider-badge {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(205, 133, 63, 0.3);
    }

    .settings-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .success-message {
        background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(34, 139, 34, 0.3);
    }

    .input-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }

    .sidebar-section {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .stButton > button {
        background: linear-gradient(135deg, #CD853F 0%, #DEB887 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(205, 133, 63, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(205, 133, 63, 0.5);
    }

    .provider-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Multi-AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Multi-AI Chatbot</h1>
    <p>Chat with multiple AI providers in one beautiful interface</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for options
with st.sidebar:
    st.markdown("### 🗂️ Options")

    with st.container():
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Provider selection and API key management
    if st.session_state.api_key:
        with st.container():
            if st.button("⚙️ AI & API Settings", use_container_width=True):
                st.session_state.show_settings = not st.session_state.show_settings

        if st.session_state.show_settings:
            st.markdown("---")
            st.markdown("### 🔧 Settings")

            with st.container():
                new_provider = st.selectbox("🤖 AI Provider", AI_PROVIDERS, key="sidebar_provider_select")
                if new_provider != st.session_state.provider:
                    st.session_state.provider = new_provider
                    st.session_state.api_key = ""
                    st.session_state.chat_history = []
                    st.session_state.show_settings = False
                    st.session_state.show_api_success = False
                    st.rerun()

                new_api_key = st.text_input(f"🔑 {new_provider} API Key", type="password", key="sidebar_api_key_input")
                if new_api_key:
                    st.session_state.api_key = new_api_key
                    st.session_state.show_api_success = True
                    st.session_state.show_settings = True
                    st.rerun()

                if st.session_state.show_api_success:
                    st.markdown('<div class="success-message">✅ API key set successfully!</div>',
                                unsafe_allow_html=True)
                    st.session_state.show_api_success = False
    else:
        st.session_state.show_settings = True

# Main content area
if not st.session_state.api_key or st.session_state.show_settings:
    # Setup page
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🚀 Get Started")

        # Provider selection with icons
        provider_icons = {"Claude": "🧠", "OpenAI": "🤖", "Gemini": "⭐", "Groq": "⚡"}
        provider = st.selectbox("Choose your AI provider:", AI_PROVIDERS, key="main_provider_select")
        st.session_state.provider = provider

        st.markdown(f"<div class='provider-badge'>{provider_icons.get(provider, '🤖')} {provider}</div>",
                    unsafe_allow_html=True)

        st.markdown(f"### 🔑 Enter your {provider} API key")
        api_key = st.text_input(f"{provider} API Key", type="password", key="main_api_key_input", placeholder="sk-...")

        if api_key:
            st.session_state.api_key = api_key
            st.session_state.show_api_success = True
            st.session_state.show_settings = False
            st.rerun()

        if st.session_state.show_api_success:
            st.markdown('<div class="success-message">✅ API key set successfully!</div>', unsafe_allow_html=True)
            st.session_state.show_api_success = False

        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.api_key and not st.session_state.show_settings:
    # Chat interface
    provider_icons = {"Claude": "🧠", "OpenAI": "🤖", "Gemini": "⭐", "Groq": "⚡"}
    current_provider = st.session_state.provider

    # Header with provider info
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="provider-badge">
                {provider_icons.get(current_provider, '🤖')} Chatting with {current_provider}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat container
    chat_container = st.container()

    with chat_container:
        if st.session_state.chat_history:
            for idx, message in enumerate(st.session_state.chat_history):
                role, text = message
                timestamp = datetime.now().strftime("%H:%M")

                if role == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <div style="font-weight: bold; margin-bottom: 0.5rem;">You</div>
                        <div>{text}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem;">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <div style="font-weight: bold; margin-bottom: 0.5rem; color: #CD853F;">
                            {provider_icons.get(current_provider, '🤖')} {current_provider}
                        </div>
                        <div>{text}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem;">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <h3>👋 Welcome to Multi-AI Chatbot!</h3>
                <p>Start a conversation with your chosen AI provider below.</p>
            </div>
            """, unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("💬 Type your message here...", key="user_input_form",
                                       placeholder="Ask me anything...")
        with col2:
            submitted = st.form_submit_button("🚀 Send", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted and user_input:
        st.session_state.chat_history.append(("user", user_input))
        # Show thinking message
        thinking_msg = f"{current_provider} is thinking..."
        st.session_state.chat_history.append(("ai", thinking_msg))
        st.rerun()

    # Replace thinking message with real response after rerun
    if st.session_state.chat_history and st.session_state.chat_history[-1][1].endswith("is thinking..."):
        last_user_msg = None
        for role, text in reversed(st.session_state.chat_history):
            if role == "user":
                last_user_msg = text
                break

        ai_response = ""
        provider = st.session_state.provider

        if provider == "Gemini":
            if genai is None:
                ai_response = "❌ Google GenAI SDK not installed. Please install it with: `pip install google-genai`"
            else:
                os.environ["GEMINI_API_KEY"] = st.session_state.api_key
                try:
                    client = genai.Client()
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=last_user_msg
                    )
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"❌ Gemini API error: {str(e)}"

        elif provider == "OpenAI":
            if OpenAI is None:
                ai_response = "❌ OpenAI SDK not installed. Please install it with: `pip install openai`"
            else:
                try:
                    client = OpenAI(api_key=st.session_state.api_key)
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": last_user_msg}]
                    )
                    ai_response = completion.choices[0].message.content
                except Exception as e:
                    ai_response = f"❌ OpenAI API error: {str(e)}"

        elif provider == "Claude":
            if anthropic is None:
                ai_response = "❌ Anthropic SDK not installed. Please install it with: `pip install anthropic`"
            else:
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    message = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": last_user_msg}]
                    )
                    ai_response = message.content[0].text if message.content else "❌ No response received"
                except Exception as e:
                    ai_response = f"❌ Claude API error: {str(e)}"

        elif provider == "Groq":
            if groq is None:
                ai_response = "❌ Groq SDK not installed. Please install it with: `pip install groq`"
            else:
                try:
                    client = groq.Groq(api_key=st.session_state.api_key)
                    chat_completion = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[{"role": "user", "content": last_user_msg}]
                    )
                    ai_response = chat_completion.choices[0].message.content
                except Exception as e:
                    ai_response = f"❌ Groq API error: {str(e)}"

        else:
            ai_response = f"🤖 Simulated {provider} response to: '{last_user_msg}'"

        st.session_state.chat_history[-1] = ("ai", ai_response)
        st.rerun()

else:
    st.info("🔑 Please enter your API key to start chatting.")
