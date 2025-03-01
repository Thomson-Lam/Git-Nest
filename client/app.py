import streamlit as st

# Apply Custom CSS for Styling
st.markdown(
    """
    <style>
        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            border-radius: 10px;
            background-color: #181818;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            color: white;
        }
        .user-message {
            background-color: #303030;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
        }
        .assistant-message {
            background-color: #505050;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("🔗 GitHub Repository Chatbot")
st.write("```Enter a public GitHub repository link to analyze its code.```")

# Hidden GitHub repo link input (white bar removed)
github_link = st.text_input("GitHub Repository Link", "").strip()

# Store conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Input Box
if prompt := st.chat_input("What is up?"):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate a fake response (replace with OpenAI API if needed)
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})

# Conversation Log Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display stored messages
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(
        f'<div class="{role_class}">{message["content"]}</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
