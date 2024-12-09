import streamlit as st
import requests

# Rasa API endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

st.title("Chat with Your Rasa Bot")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List to store user queries and bot responses

# Input for the user query
user_message = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send"):
    if user_message.strip():
        try:
            # Send the user message to Rasa
            response = requests.post(
                RASA_URL,
                json={"sender": "streamlit_user", "message": user_message}
            )
            if response.status_code == 200:
                # Parse the chatbot's responses
                bot_responses = response.json()
                for bot_response in bot_responses:
                    # Append bot response to chat history
                    st.session_state.chat_history.append(("Bot", bot_response.get("text", "No response")))
            else:
                st.error("Error: Could not connect to Rasa server.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

        # Append user message to chat history
        st.session_state.chat_history.append(("You", user_message))
    else:
        st.warning("Please enter a message.")

# Display chat history
st.subheader("Chat History")
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
def paginate_responses(responses, page, page_size=10):
    start_idx = page * page_size
    end_idx = start_idx + page_size
    return responses[start_idx:end_idx]

# Display paginated chat history
page = st.number_input("Page", min_value=0, step=1, value=0)
paginated_history = paginate_responses(st.session_state.chat_history, page, 20)

for speaker, message in paginated_history:
    st.markdown(f"**{speaker}:** {message}")

# Option to reset chat history
if st.button("Clear Chat"):
    st.session_state.chat_history = []  # Clear the history
    st.success("Chat history cleared.")
if st.button("Download Chat History"):
    chat_text = "\n".join([f"{speaker}: {message}" for speaker, message in st.session_state.chat_history])
    st.download_button("Download", data=chat_text, file_name="chat_history.txt", mime="text/plain")