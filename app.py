import streamlit as st
from huggingface_hub import InferenceClient
import os

# Page configuration
st.set_page_config(
    page_title="History AI Agent",
    page_icon="🕰️",
    layout="wide"
)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are an expert History AI assistant build by Julien Okumu. 
            Your role is to:
            - Provide detailed and accurate historical information
            - Explain historical events with context and nuance
            - Use markdown formatting for clear, structured responses
            - Include relevant historical dates, figures, and insights
            - Break down complex historical topics into understandable explanations
            """
        }
    ]

# Retrieve API key
api_key = os.getenv('fake_api')

# Streamlit UI
def main():
    # Page title and description
    st.title("🕰️ History AI Agent |  Julien Okumu")
    st.markdown("""
    ### Explore the Depths of Human History
    - Ask any historical question
    - Receive detailed, markdown-formatted responses
    - Discover insights across different historical periods and civilizations
    """)

    # Sidebar for additional information
    st.sidebar.header("About History Guru AI")
    st.sidebar.info("""
    🌍 An AI-powered historical knowledge agent build by Julien Okumu
    - Comprehensive historical insights
    - Markdown-formatted responses
    - Powered by advanced AI technology
    """)

    # Chat input
    user_input = st.chat_input("Ask a historical question...")

    # Process user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response
        with st.chat_message("History AI Agent"):
            # Placeholder for streaming response
            response_placeholder = st.empty()
            
            # Prepare full response
            full_response = ""
            
            try:
                # Initialize Hugging Face client
                client = InferenceClient(api_key=api_key)

                # Stream the response
                stream = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-1B-Instruct", 
                    messages=st.session_state.messages, 
                    max_tokens=500,
                    stream=True
                )

                # Collect and display streamed response
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response)

                # Final markdown response
                response_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                full_response = "I apologize, but there was an error processing your request."

        # Add AI response to chat history
        st.session_state.messages.append({
            "role": "History AI Agent", 
            "content": full_response
        })

# Run the Streamlit app
if __name__ == "__main__":
    main()