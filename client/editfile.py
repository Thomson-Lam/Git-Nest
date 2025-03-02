import requests
import json
import base64
import re
import os
from dotenv import load_dotenv  # Import dotenv to load .env variables

# Load environment variables from .env file
load_dotenv()

# Retrieve GitHub token from .env
GITHUB_TOKEN = os.getenv("GITHUB_PAT")

# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com/repos"

def update_github_file(repo_url, file_path, new_content):
    """
    Updates a file in a GitHub repository using a token from .env.
    
    Parameters:
        repo_url (str): The GitHub repository URL.
        file_path (str): The path to the file in the repository.
        new_content (str): The new content to be written to the file.
    """
    if not GITHUB_TOKEN:
        print("GitHub token not found in .env file! Make sure it's set.")
        return
    
    # Extract owner and repo name from URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        print("Invalid GitHub repository URL.")
        return
    
    owner, repo = match.groups()
    
    # Construct API URLs
    file_api_url = f"{GITHUB_API_BASE}/{owner}/{repo}/contents/{file_path}"

    # Set up authentication headers
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Step 1: Get the current file metadata (including SHA)
    response = requests.get(file_api_url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]  # Required for updating the file
    elif response.status_code == 401:
        print("401 Unauthorized: Check your GitHub token in .env.")
        return
    elif response.status_code == 404:
        print("File not found. Make sure the path is correct.")
        return
    else:
        print(f"Failed to fetch file details. Status Code: {response.status_code}")
        return
    
    # Step 2: Prepare updated file content (base64 encoding required by GitHub API)
    encoded_content = base64.b64encode(new_content.encode()).decode()

    # Step 3: Create the request payload
    update_payload = {
        "message": f"Updating {file_path} via API",
        "content": encoded_content,
        "sha": sha  # Required to avoid conflicts
    }

    # Step 4: Send PUT request to update the file
    update_response = requests.put(file_api_url, headers=headers, json=update_payload)

    if update_response.status_code == 200:
        print(f"Successfully updated {file_path} in {repo}!")
    else:
        print(f"Failed to update the file. Status Code: {update_response.status_code}")

# Example usage
# repo_url = input("Enter the GitHub repository URL: ")
# file_path = input("Enter the path to the file (e.g., folder1/anothertest.py): ")
# new_content = input("Enter the new content for the file: ")

# update_github_file(repo_url, file_path, new_content)
