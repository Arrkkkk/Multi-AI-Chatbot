import streamlit as st
import os

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
AI_PROVIDERS = ["Claude", "OpenAI", "Gemini", "Grok"]

st.set_page_config(page_title="Multi-AI Chatbot", page_icon="🤖")
st.title("🤖 Multi-AI Chatbot")

# Sidebar for options
with st.sidebar:
    st.header("🗂️ Options")
    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()
    # If API key is set, show settings button
    if st.session_state.api_key:
        if st.button("AI & API Settings"):
            st.session_state.show_settings = not st.session_state.show_settings
        if st.session_state.show_settings:
            st.markdown("---")
            st.subheader("Change AI Provider")
            new_provider = st.selectbox("AI Provider", AI_PROVIDERS, key="sidebar_provider_select")
            if new_provider != st.session_state.provider:
                st.session_state.provider = new_provider
                st.session_state.api_key = ""
                st.session_state.chat_history = []
                st.session_state.show_settings = False
                st.session_state.show_api_success = False
                st.rerun()
            new_api_key = st.text_input(f"{new_provider} API Key", type="password", key="sidebar_api_key_input")
            if new_api_key:
                st.session_state.api_key = new_api_key
                st.session_state.show_api_success = True
                st.session_state.show_settings = True
                st.rerun()
            if st.session_state.show_api_success:
                st.success("API key set!", icon="✅")
                st.session_state.show_api_success = False
    else:
        st.session_state.show_settings = True

# Main area
if not st.session_state.api_key or st.session_state.show_settings:
    st.subheader("1. Choose your AI provider:")
    provider = st.selectbox("AI Provider", AI_PROVIDERS, key="main_provider_select")
    st.session_state.provider = provider
    st.subheader(f"2. Enter your {provider} API key:")
    api_key = st.text_input(f"{provider} API Key", type="password", key="main_api_key_input")
    if api_key:
        st.session_state.api_key = api_key
        st.session_state.show_api_success = True
        st.session_state.show_settings = False
        st.rerun()
    if st.session_state.show_api_success:
        st.success("API key set!", icon="✅")
        st.session_state.show_api_success = False

if st.session_state.api_key and not st.session_state.show_settings:
    st.subheader(f"Chat with {st.session_state.provider}")
    for idx, message in enumerate(st.session_state.chat_history):
        role, text = message
        if role == "user":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**{st.session_state.provider}:** {text}")
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", key="user_input_form")
        submitted = st.form_submit_button("Send")
    if submitted and user_input:
        st.session_state.chat_history.append(("user", user_input))
        # Show thinking message
        thinking_msg = f"{st.session_state.provider} is thinking..."
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
                ai_response = "[google-genai SDK not installed]"
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
                    ai_response = f"[Gemini API error: {e}]"
        elif provider == "OpenAI":
            if OpenAI is None:
                ai_response = "[openai SDK not installed]"
            else:
                try:
                    client = OpenAI(api_key=st.session_state.api_key)
                    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": last_user_msg}])
                    ai_response = completion.choices[0].message.content
                except Exception as e:
                    ai_response = f"[OpenAI API error: {e}]"
        elif provider == "Claude":
            if anthropic is None:
                ai_response = "[anthropic SDK not installed]"
            else:
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    message = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": last_user_msg}]
                    )
                    ai_response = message.content[0].text if message.content else "[No response]"
                except Exception as e:
                    ai_response = f"[Claude API error: {e}]"
        elif provider == "Grok":
            if groq is None:
                ai_response = "[groq SDK not installed]"
            else:
                try:
                    client = groq.Groq(api_key=st.session_state.api_key)
                    chat_completion = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[{"role": "user", "content": last_user_msg}]
                    )
                    ai_response = chat_completion.choices[0].message.content
                except Exception as e:
                    ai_response = f"[Groq API error: {e}]"
        else:
            ai_response = f"[Simulated {provider} response to: '{last_user_msg}']"
        st.session_state.chat_history[-1] = ("ai", ai_response)
        st.rerun()
else:
    st.info("Please enter your API key to start chatting.") 