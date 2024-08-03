import json
import uuid

import requests
import streamlit as st

# FastAPI endpoint URL
CHAT_API_URL = "http://127.0.0.1:8000/api/chat/chat"

st.title("Chat with Restaurant Agent")

# Initialize session state for managing chat threads
if "threads" not in st.session_state:
    st.session_state["threads"] = {}


# Function to send message to FastAPI chat endpoint
def send_message(message, thread_id):
    """
    Send the user message to the FastAPI chat endpoint.

    :param message: The user message
    :param thread_id: The thread ID

    :yield: The assistant response
    """
    response = requests.post(
        CHAT_API_URL,
        json={"message": message, "thread_id": thread_id},
        stream=True,
        timeout=30,
    )
    if response.status_code == 200:
        assistant_response = ""
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                chunk_data = json.loads(chunk)
                assistant_response = chunk_data["content"]
        yield assistant_response
    else:
        yield "Error: Could not get response from the server."


# Create a new thread
if st.button("Create New Thread"):
    thread_id = str(uuid.uuid4())
    st.session_state["threads"][thread_id] = []
    st.rerun()

# Select a thread
thread_ids = list(st.session_state["threads"].keys())
selected_thread_id = st.selectbox("Select Thread", thread_ids)

# Input area for user message
user_message = st.text_input("You:", "")

# If the user submits a message
if st.button("Send"):
    if user_message and selected_thread_id in st.session_state["threads"]:
        # Append user message to the selected thread
        st.session_state["threads"][selected_thread_id].append(
            {"role": "user", "content": user_message},
        )

        # Get response from FastAPI chat endpoint
        assistant_response = next(send_message(user_message, selected_thread_id))

        # Append the assistant response to the selected thread
        st.session_state["threads"][selected_thread_id].append(
            {"role": "assistant", "content": assistant_response},
        )

# Display chat messages for the selected thread
if selected_thread_id in st.session_state["threads"]:
    for i, message in enumerate(st.session_state["threads"][selected_thread_id]):
        if message["role"] == "user":
            st.text_area(
                "You",
                message["content"],
                height=75,
                key=f"user_{selected_thread_id}_{i}",
            )
        else:
            st.text_area(
                "Restaurant Agent",
                message["content"],
                height=75,
                key=f"assistant_{selected_thread_id}_{i}",
            )

# Delete the selected thread
if st.button("Delete Thread"):
    if selected_thread_id in st.session_state["threads"]:
        del st.session_state["threads"][selected_thread_id]
        st.rerun()
