
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

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)

# Main chat interface setup
st.title("NSCLC Insights")


def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    
    message_content = message.content[0].text
    annotations = message_content.annotations if hasattr(message_content, 'annotations') else []

    # Add footnotes to the end of the message content
    full_response = message_content.value 
    return full_response
    
# Only show the chat interface if the chat has been started
if st.session_state.start_chat:
    # Initialize the model and messages list if not already in session state
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Chat input for the user
    if prompt := st.chat_input("What insights would you like to unlock?"):
        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create a run with additional instructions
        run = client.beta.threads.runs.create(thread_id=st.session_state.thread_id,
                                              assistant_id=assistant_id)

        # Poll for the run to complete and retrieve the assistant's messages


        while True:
            run = client.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)

            if run.status=="completed":
                messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
                print(messages)
                break;

        # Retrieve messages added by the assistant
        latest_message = messages.data[0]

        for content in latest_message.content:
                if hasattr(content, 'image_file'):
                  a=content.image_file.file_id
                  api_response = client.files.with_raw_response.retrieve_content(a)
                  if api_response.status_code == 200:
                    content2 = api_response.content
                  with open('image.png', 'wb') as f:
                    f.write(content2)
                  print('File downloaded successfully.')
                  print(a)
                  im = Image.open('image.png')
                  st.image(im)
        for content in latest_message.content:
            if hasattr(content, 'text'):
                full_response=content.text.value
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)
                break;
else:
    # Prompt to start the chat
    st.write("Please click 'Start Chat' to begin the conversation.")

# Custom CSS for Quilt.AI inspired styling
st.markdown(
    '''
    <style>
    /* Overall page styling */
    body {
        font-family: 'Arial', sans-serif;
        color: #333;
        background-color: #fff;
    }

    /* Chat box styling */
    .chat-box {
        background-color: #fff;
        border: 1px solid #d0d7de;
        border-radius: 10px;
        padding: 15px;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Message styling */
    .message {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        line-height: 1.4;
        font-size: 16px;
    }
    .user-message {
        background-color: #eff6ff;
        color: #0366d6;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
    }
    .bot-message {
        background-color: #f6f8fa;
        color: #24292e;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
    }

    /* Input area styling */
    .stTextInput>div>div>input {
        padding: 10px;
        border-radius: 20px;
        border: 1px solid #d1d5da;
        font-size: 16px;
    }

    /* Button styling */
    button {
        border-radius: 20px;
        border: none;
        color: white;
        background-color: #0366d6;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
        color: white;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Redesigning the chat interface with Quilt.AI inspired aesthetics
# (The chat display and input area will be styled and organized as per the new advanced design)
