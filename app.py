import streamlit as st
from chatbot import ChatBot
from gtts import gTTS
import base64
import PyPDF2 
from io import BytesIO
import time 

# --- PAGE CONFIG (Centered Default) ---
st.set_page_config(
    page_title="Lily AI",
    page_icon="✨",
    initial_sidebar_state="expanded"
)

def autoplay_audio(text):
    try:
        tts = gTTS(text=text, lang='en', tld='com')
        sound_file = BytesIO()
        tts.write_to_fp(sound_file)
        sound_file.seek(0)
        b64 = base64.b64encode(sound_file.read()).decode()
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass


def stream_data(text):
    """Simulates typing effect like ChatGPT/Gemini"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04) 


st.markdown("""
<style>
/* FONT IMPORT */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');
* { font-family: 'Outfit', sans-serif; }

/* 1. CORE THEME */
.stApp {
    background-color: #131314;
    color: #E3E3E3;
}

/* 2. REMOVE TOP PADDING (Cleaner Look) */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* 3. INPUT FIELD CONTAINER FIX (Jaisa aapne bataya) */
/* This targets the inner container which might have a default border */
.st-emotion-cache-x1bvup, .st-emotion-cache-1c7v0s0 {
    border: none !important; 
    box-shadow: none !important;
}


/* 4. INPUT FIELD (Floating Pill - Centered Optimized) */
div[data-testid="stChatInput"] {
    background-color: #1E1F20 !important;
    border: 1px solid #444746 !important; 
    border-radius: 30px !important;
    padding: 5px 10px;
}
/* Blue Glow on Focus */
div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #4285F4 !important;
    box-shadow: 0 0 15px rgba(66, 133, 244, 0.2) !important;
}

/* 5. SUGGESTION CARDS (GRID FIX FOR CENTERED LAYOUT) */
.card-container {
    display: grid;
    /* Forces 2 columns on desktop, 1 on mobile */
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-top: 30px;
}

.suggestion-card {
    background-color: #1E1F20;
    padding: 15px 20px;
    border-radius: 16px; /* Softer rounded corners */
    border: 1px solid #333;
    transition: all 0.3s ease;
    cursor: pointer;
    /* Height adjustment */
    min-height: 100px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 8px;
}

.suggestion-card:hover {
    background-color: #28292a;
    border-color: #555;
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.card-icon {
    font-size: 24px;
    margin-bottom: 8px;
}
.card-text {
    font-size: 14px;
    font-weight: 500;
    color: #E3E3E3;
    line-height: 1.4;
}

/* 6. ANIMATED WELCOME TITLE */
@keyframes gradient-animation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.lily-title {
    font-size: 48px; /* Slightly smaller for centered view */
    font-weight: 700;
    background: linear-gradient(270deg, #4285F4, #9B72CB, #D96570, #4285F4);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-animation 6s ease infinite;
    margin-bottom: 0px;
}
.lily-sub {
    font-size: 27px;
    color: #9aa0a6;
    margin-top: 5px;
    font-weight: 400;
}

/* 7. CHAT BUBBLES (Compact) */
[data-testid="stChatMessage"]:nth-child(odd) {
    background-color: #1E1F20; 
    border-radius: 20px 20px 4px 20px;
    padding: 10px 15px;
    margin-top: 2px;
    border: 1px solid #333;
}
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: transparent;
    padding-left: 0;
}

/* Hide User Avatar */
[data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageAvatar"] {
    display: none !important;
}

/* Hide Scrollbars */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if "lily" not in st.session_state:
    st.session_state.lily = ChatBot(name="Lily")
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚡ Controls")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.lily.pdf_context = ""
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    enable_voice = st.toggle("Voice Mode", value=True)
    
    st.markdown("---")
    # File uploader label removed for cleaner look
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.session_state.lily.pdf_context = text
            st.toast("Brain Updated!", icon="🧠")
        except:
            st.error("Error reading PDF.")

# --- WELCOME SCREEN ---
if len(st.session_state.messages) == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="lily-title">Hello, Ibi.</span>', unsafe_allow_html=True)
    st.markdown('<div class="lily-sub">How can Lily assist you today?</div>', unsafe_allow_html=True)

    
    st.markdown("""
    <div class="card-container">
        <div class="suggestion-card">
            <span class="card-icon">🐍</span>
            <span class="card-text">Write a Python Script</span>
        </div>
        <div class="suggestion-card">
            <span class="card-icon">📝</span>
            <span class="card-text">Summarize this Document</span>
        </div>
        <div class="suggestion-card">
            <span class="card-icon">🌍</span>
            <span class="card-text">Plan a Trip to Japan</span>
        </div>
        <div class="suggestion-card">
            <span class="card-icon">💡</span>
            <span class="card-text">Give me Startup Ideas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    role = message["role"]
    avatar = "✨" if role == "assistant" else None
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# --- INPUT AREA ---
user_input = st.chat_input("Ask Lily anything...")

if user_input:
    # 1. User Message 
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Bot Response
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        
        try:
            full_response = st.session_state.lily.process_input(user_input)
            
            # Streaming Logic
            streamed_text = ""
            for chunk in stream_data(full_response):
                streamed_text += chunk
                message_placeholder.markdown(streamed_text + "▌") 
            
            message_placeholder.markdown(full_response) 
            
            if enable_voice:
                autoplay_audio(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            message_placeholder.markdown("Connection Error.")