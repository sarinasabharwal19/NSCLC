
from openai import OpenAI
import os
import streamlit as st
import time
from PIL import Image

client = OpenAI(api_key=os.environ['OPEN_API_KEY'])
assistant_id = os.environ['ASSIS_ID']

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="NSCLC Insights", page_icon=":speech_balloon:")

# Start chat button in the sidebar
if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)

# Main chat interface setup
st.title("NSCLC Insights")

# Function to process messages (remains unchanged)
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    
    message_content = message.content[0].text
    annotations = message_content.annotations if hasattr(message_content, 'annotations') else []

    # Add footnotes to the end of the message content
    full_response = message_content.value 
    return full_response

# Custom CSS for styling
st.markdown(
    '''
    <style>
    .chat-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        height: 500px;
        overflow-y: auto;
    }
    .message {
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e1f5fe;
    }
    .bot-message {
        background-color: #dcedc8;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Chat display area
with st.container():
    chat_history = st.empty()
    
    # Display chat history
    # ... existing code ...

# User input
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Your message", key='user_input')
    with col2:
        if st.button('Send'):
            # Process and update chat window (you'll need to implement the logic)
            
            st.session_state.chat_window += f"\nUser: {user_input}\nBot: [response]"

# Add more sections as needed
