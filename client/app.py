import streamlit as st
from dotenv import load_dotenv
import os
import time
import json
import re
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from fetchfiles import fetch_all_repo_files 
from file_content import get_file_content

# Load environment variables
load_dotenv()
key = os.getenv("GEMINI_API_KEY")

# Ensure API key is loaded
if not key:
    st.error("GEMINI_API_KEY is missing. Check your .env file.")
    st.stop()

# Configure Google Generative AI
genai.configure(api_key=key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("🔗 GitHub Repository Chatbot")
st.write("```Enter a public GitHub repository link to analyze its code.```")

# GitHub repo link input
github_link = st.text_input("Paste your GitHub Repository Link", "").strip()

from urllib.parse import urlparse

def extract_github_details(github_url):
    """
    Extracts repo_owner and repo_name from a GitHub repository URL.
    """
    try:
        parsed_url = urlparse(github_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            return path_parts[0], path_parts[1]
        else:
            return None, None
    except Exception as e:
        return None, None

# Initialize repository variables
repo_owner, repo_name = extract_github_details(github_link)

# Function to read JSON files from disk
def read_json_files(json_filename: str) -> dict:
    """
    Reads a JSON file and returns its content.
    """
    try:
        with open(json_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"error": f"File '{json_filename}' not found."}
    except json.JSONDecodeError:
        return {"error": f"Failed to decode JSON. Check the file format."}

# Fetch repo files if a GitHub repo link is provided
if github_link:
    status_placeholder = st.empty()
    status_placeholder.write("🔄 Fetching repository data...")
    fetch_all_repo_files(github_link)  # This saves the repo data to a JSON file
    status_placeholder.write("✅ Data Updated")

# Define the tool for reading JSON files
read_json_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="read_json_files",
            description="Reads and returns the contents of a JSON file.",
            parameters={
                "type": "object",
                "properties": {
                    "json_filename": {
                        "type": "string",
                        "description": "The path to the JSON file."
                    }
                },
                "required": ["json_filename"]
            }
        )
    ]
)

# Define the tool for retrieving specific file content
get_file_content_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="get_file_content",
            description="Retrieves the content of a specific file from a JSON structure that stores GitHub repository data.",
            parameters={
                "type": "object",
                "properties": {
                    "json_file": {
                        "type": "string",
                        "description": "Path to the JSON file that stores GitHub repository file contents."
                    },
                    "repo_owner": {
                        "type": "string",
                        "description": "The owner of the repository (e.g., 'MrPumpkin92')."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "The name of the repository (e.g., 'test')."
                    },
                    "file_path": {
                        "type": "string",
                        "description": "The path to the specific file within the repository (e.g., 'folder1/anothertest.py')."
                    }
                },
                "required": ["json_file", "repo_owner", "repo_name", "file_path"]
            }
        )
    ]
)

# Store conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Input Box with Tool Integration
prompt = st.chat_input("Ask me anything about the repository (e.g., 'List all files')...")

if prompt:
    st.session_state.messages.append({"role": "user", "user-message": prompt})

    if "json" in prompt.lower() or "json file" in prompt.lower():
        json_filename = "github_file_contents.json"  # Fixed file path
        json_data = read_json_files(json_filename)
        response_text = f"**Here is the JSON content:**\n\n```json\n{json.dumps(json_data, indent=4)}\n```"
    elif "content" in prompt.lower() or "read file content" in prompt.lower():
        # Updated regex to correctly extract the file path (e.g., test.py)
        file_path_match = re.search(
            r'(?:read file content(?: in)?|content(?: of file)?(?: in)?)\s+([\w\-/\.]+)', 
            prompt, 
            re.IGNORECASE
        )
        if file_path_match:
            file_path = file_path_match.group(1)
            json_filename = "github_file_contents.json"
            file_data = get_file_content(json_filename, repo_owner, repo_name, file_path)
            # Attempt to load file_data as JSON if applicable; if not, use it directly
            try:
                parsed_data = json.loads(file_data)
                output_data = json.dumps(parsed_data, indent=4)
            except (json.JSONDecodeError, TypeError):
                output_data = file_data
            response_text = f"**Here is the file content:**\n\n```json\n{output_data}\n```"
        else:
            response_text = "Could not extract the file path from your prompt. Please specify the file path (e.g., 'read file content in test.py')."
    else:
        # Let Gemini process the query and invoke tools if needed
        response = model.generate_content(
            contents=prompt,
            tools=[read_json_tool, get_file_content_tool]
        )
        response_text = response.text

    st.session_state.messages.append({"role": "assistant", "response": response_text})

# Display Full Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        text_content = message.get("user-message") or message.get("response")
        # Apply code block formatting only for JSON/structured data messages
        if text_content.startswith("**Here is the JSON content:**") or text_content.startswith("**Here is the file content:**"):
            st.markdown(text_content)
        else:
            st.markdown(text_content)

# Conversation Log Container (for potential future styling)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
