from openai import OpenAI
import os
import streamlit as st
import time
from PIL import Image



client = OpenAI(api_key='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')
#OLD_assistant_id = 'asst_WqSuz6btalCwiCtkU04WL0gK'
assistant_id = 'asst_egYjXGjE44ugosGpHC1uugls'
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