import streamlit as st
import os
import io
# from dotenv import load_dotenv

# load_dotenv()
# HF_API_KEY = os.getenv('HF_API_KEY')

def get_user_api_key():
    with st.sidebar:
        OPENAI_API_KEY = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
        "[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)"
        
        HF_API_KEY = st.text_input("HuggingFace API Key", key="huggingface_api_key", type="password")
        "[Get a Hugging Face API Key](https://huggingface.co/docs/hub/en/security-tokens)"
        
        return OPENAI_API_KEY, HF_API_KEY

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
    
    user_text = st.text_area(
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

def generate_response(user_text, selected_server, server_url, OPENAI_API_KEY, HF_API_KEY):
    """Generate response using OpenAI client"""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    
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


def main():
    # Initialize page layout
    main_column = initialize_page()

    OPENAI_API_KEY, HF_API_KEY = get_user_api_key()
    
    # Get transcript input
    user_text = get_user_input(main_column)
    
    # Get server selection
    selected_server, server_url = create_mcp_server_dropdown()
    
    # Generate response
    if st.button("Generate Response", key="generate_button"):
        if user_text:
            with st.spinner("Generating response..."):
                response = generate_response(user_text, selected_server, server_url, OPENAI_API_KEY, HF_API_KEY)

        else:
            st.warning("Please enter a topic first.")

if __name__ == "__main__":
    main()