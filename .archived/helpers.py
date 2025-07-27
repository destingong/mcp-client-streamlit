import streamlit as st

def create_mcp_server_dropdown():
    # Define a list of MCP servers
    # You can modify this list according to your actual server configurations
    mcp_servers = {
        "deepwiki": "https://mcp.deepwiki.com/mcp",
        "huggingface": "https://huggingface.co/mcp"
    }

    # # Create a dropdown (selectbox) for server selection
    # selected_server = st.selectbox(
    #     "Select MCP Server",
    #     options=list(mcp_servers.keys()),
    #     help="Choose the MCP server you want to connect to"
    # )

    # Create radio buttons for server selection
    selected_server = st.radio(
        "Select MCP Server",
        options=list(mcp_servers.keys()),
        help="Choose the MCP server you want to connect to"
    )

    # Get the selected server URL
    server_url = mcp_servers[selected_server]
    
    return selected_server, server_url