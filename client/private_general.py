import requests
import json
import re

def fetch_github_repo_with_auth(url, token):
    # Extract owner and repo name from the URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        print("Invalid GitHub repository URL.")
        return
    
    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Set up headers for authentication
    headers = {"Authorization": f"token {token}"}

    # Make the API request
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()

        # Save data to a JSON file
        json_filename = f"{repo}_repo_data.json"
        with open(json_filename, "w") as json_file:
            json.dump(repo_data, json_file, indent=4)
        
        print(f"Repository data saved to {json_filename}")
    elif response.status_code == 404:
        print("Repository not found. Check if it's private or the URL is incorrect.")
    elif response.status_code == 401:
        print("Authentication failed. Check your GitHub token.")
    else:
        print(f"Failed to fetch repository data. Status Code: {response.status_code}")

# Example usage
repo_url = input("Enter a GitHub repository URL: ")
access_token = input("Enter your GitHub Personal Access Token: ")  # 🔐 Securely input your PAT
fetch_github_repo_with_auth(repo_url, access_token)
