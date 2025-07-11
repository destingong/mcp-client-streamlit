import streamlit as st
import os
import io
import boto3
from dotenv import load_dotenv
import helpers

load_dotenv()
HF_API_KEY = os.getenv('HF_API_KEY')

def initialize_page():
    """Initialize the Streamlit page configuration and layout"""
    st.set_page_config(
        page_icon="🤖",
        layout="centered"
    )
    st.title("Streamlit MCP Client")
    
    return st.columns(1)[0]

def get_user_input(column):
    """Handle transcript input methods and return the transcript text"""
    
    user_text = column.text_area(
        "Please enter the topics you’re interested in:",
        height=100,
        placeholder="Type it here..."
    )
    
    return user_text

def create_mcp_server_dropdown():
    # Define a list of MCP servers
    mcp_servers = {
        "deepwiki": "https://mcp.deepwiki.com/mcp",
        "huggingface": "https://huggingface.co/mcp"
    }

    selected_server = st.radio(
        "Select MCP Server",
        options=list(mcp_servers.keys()),
        help="Choose the MCP server you want to connect to"
    )

    # Get the selected server URL
    server_url = mcp_servers[selected_server]
    
    return selected_server, server_url

def generate_response(user_text, selected_server, server_url):
    """Generate response using OpenAI client"""
    from openai import OpenAI

    client = OpenAI()
    
    try:
        if selected_server == 'huggingface':
            response = client.responses.create(
                model="gpt-3.5-turbo",
                tools=[{
                    "type": "mcp",
                    "server_label": selected_server,
                    "server_url": server_url,
                    "require_approval": "never",
                    "headers": {
                        "Authorization": f"Bearer {HF_API_KEY}"
                    }
                }],
                input=f"List some resources relevant to this topic: {user_text}?"
            )
        else:
            response = client.responses.create(
                model="gpt-3.5-turbo",
                tools=[{
                    "type": "mcp",
                    "server_label": selected_server,
                    "server_url": server_url,
                    "require_approval": "never",
                }],
                input=f"Summarize codebase contents relevant to this topic: {user_text}?"
            )

        st.info(
            f"""
            **Response:**
            {response.output_text}
            """
        )
        return response
        
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

# def display_video_info(user_text, response):
#     """Display response"""
#     if response:
#         st.info(
#             f"""
#             **Response:**
#             {response.output_text}
#             """
#         )
#     else:
#         st.error("No responses have been generated.")

def main():
    # Initialize page layout
    main_column = initialize_page()
    
    # Get transcript input
    user_text = get_user_input(main_column)
    
    # Get server selection
    with main_column:
        selected_server, server_url = helpers.create_mcp_server_dropdown()
    
    # Generate response
    if st.button("Generate Response", key="generate_button"):
        if user_text:
            with st.spinner("Generating response..."):
                response = generate_response(user_text, selected_server, server_url)

        else:
            st.warning("Please enter a topic first.")

if __name__ == "__main__":
    main()