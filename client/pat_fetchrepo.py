import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_github_repos():
    """
    Fetch all repositories of the authenticated user using a GitHub PAT stored in .env.
    
    :return: List of repository names with their URLs
    """
    pat = os.getenv("GITHUB_PAT")  # Load PAT from .env file
    if not pat:
        print("Error: GITHUB_PAT not found in .env file")
        return None

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        repo_list = [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]
        return repo_list
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
repos = list_github_repos()

if repos:
    for repo in repos:
        print(f"Repo Name: {repo['name']} - URL: {repo['url']}")
