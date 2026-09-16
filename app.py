import streamlit as st
from Chat_with_Me import Chatbot


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ZERO Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
/* =========================
   GLOBAL
========================= */
.stApp {
    background: #0b0f14;
    color: #ffffff;
}

.block-container {
    max-width: 1200px;
    padding-top: 25px;
    padding-bottom: 120px;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background: #10141b;
    border-right: 1px solid #252b35;
}

.sidebar-logo {
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin-bottom: 3px;
}

.sidebar-subtitle {
    color: #7f8998;
    font-size: 13px;
    margin-bottom: 35px;
}

/* =========================
   TOP BAR
========================= */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 5px 20px 5px;
}

.brand {
    font-size: 25px;
    font-weight: 700;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #11161d;
    border: 1px solid #29303a;
    border-radius: 20px;
    padding: 7px 14px;
    color: #a7afbb;
    font-size: 13px;
}

.status-dot {
    width: 9px;
    height: 9px;
    background: #20c76b;
    border-radius: 50%;
}

/* =========================
   WELCOME
========================= */
.welcome-container {
    max-width: 780px;
    margin: 80px auto 45px auto;
    text-align: center;
}

.welcome-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.welcome-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
}

.welcome-subtitle {
    color: #8b95a4;
    font-size: 15px;
    line-height: 1.7;
}

/* =========================
   CHAT
========================= */
.user-row {
    display: flex;
    justify-content: flex-end;
    margin: 18px 0;
}

.user-message {
    max-width: 75%;
    background: #202733;
    color: white;
    padding: 13px 18px;
    border-radius: 18px 18px 4px 18px;
    line-height: 1.6;
    font-size: 15px;
}

.bot-row {
    display: flex;
    justify-content: flex-start;
    margin: 18px 0;
}

.bot-message {
    max-width: 78%;
    background: #151a22;
    border: 1px solid #272e38;
    color: #e9edf2;
    padding: 15px 18px;
    border-radius: 18px 18px 18px 4px;
    line-height: 1.7;
    font-size: 15px;
}

/* =========================
   SIDEBAR BUTTON
========================= */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    background: #171c24;
    border: 1px solid #2a313c;
    color: white;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #596372;
}

/* =========================
   SELECTBOX
========================= */
div[data-baseweb="select"] > div {
    background: #171c24;
    border-color: #2a313c;
    color: white;
}

/* =========================
   CHAT INPUT
========================= */
div[data-testid="stChatInput"] {
    background: #10141b;
    border-top: 1px solid #202631;
    padding-top: 14px;
}

div[data-testid="stChatInput"] textarea {
    background: #171c24;
    color: white;
    border: 1px solid #303744;
}

/* =========================
   HIDE STREAMLIT UI
========================= */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot(personality="Happy")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">🤖 ZERO</div>
        <div class="sidebar-subtitle">AI Assistant</div>
        """,
        unsafe_allow_html=True,
    )

    # New Chat
    if st.button("＋  New Chat", use_container_width=True):
        st.session_state.chatbot.clear_chat()
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("")

    # Personality
    st.markdown("### Personality")
    personality = st.selectbox(
        "Choose personality",
        ["Happy", "Sad", "Angry", "Professional", "Funny"],
        label_visibility="collapsed",
    )
    st.session_state.chatbot.set_personality(personality)

    st.markdown("---")

    # Current mode
    emoji = {
        "Happy": "😊",
        "Sad": "😔",
        "Angry": "😠",
        "Professional": "💼",
        "Funny": "😂",
    }

    st.markdown("### Current Mode")
    st.markdown(f"**{emoji[personality]} {personality}**")

    st.markdown("---")

    # Conversation count
    st.markdown("### Conversation")
    count = len(st.session_state.chat_history)

    if count == 0:
        st.caption("No messages yet.")
    else:
        st.caption(f"{count} messages")

    st.markdown("---")

    st.caption("ZERO AI Assistant")
    # st.caption("Gemini + LangChain")


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
    <div class="topbar">
        <div class="brand">🤖 ZERO</div>
        <div class="status">
            <span class="status-dot"></span>
            Online
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.chat_history:
    st.markdown(
        """
        <div class="welcome-container">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-title">How can I help?</div>
            <div class="welcome-subtitle">
                I'm ZERO, your personal AI assistant.<br>
                Ask me anything, learn something new,
                write code, or solve a problem.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DISPLAY CHAT
# ============================================================

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="user-row">
                <div class="user-message">{message["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="bot-row">
                <div class="bot-message">🤖 &nbsp;{message["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input("Message ZERO...")


# ============================================================
# SEND MESSAGE
# ============================================================

if user_prompt:
    # Save user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # Generate answer
    with st.spinner("ZERO is thinking..."):
        answer = st.session_state.chatbot.ask(user_prompt)

    # Save assistant message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    # Refresh UI
    st.rerun()