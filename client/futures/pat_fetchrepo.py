import os
import json
import requests
from dotenv import load_dotenv

# Future

# Load environment variables from .env file
load_dotenv()

def list_github_repos():
    """
    Fetch all repositories of the authenticated user using a GitHub PAT stored in .env.
    Save the data to 'personal_repos.json', updating it each time the function runs.
    
    :return: None (data is saved to JSON file)
    """
    pat = os.getenv("GITHUB_PAT")  # Load PAT from .env file
    if not pat:
        print("Error: GITHUB_PAT not found in .env file")
        return

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        repo_list = [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]

        # Save to JSON file
        with open("personal_repos.json", "w", encoding="utf-8") as f:
            json.dump(repo_list, f, indent=4)
        
        print("Repository data updated in 'personal_repos.json'.")
    
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Call the function
list_github_repos()
