import requests
import json
import re
import os

def fetch_all_repo_files(url, json_filename="github_file_contents.json"):
    # Extract owner (username) and repo name from the URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        print("Invalid GitHub repository URL.")
        return
    
    owner, repo = match.groups()
    base_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    # Load existing JSON file if exists
    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    def get_files(api_url, path_prefix=""):
        """ Recursively fetch files from the repository. """
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            repo_data = {}

            for item in contents:
                item_path = f"{path_prefix}{item['name']}"  # Keep track of subdirectory paths

                if item["type"] == "file" and item.get("download_url"):
                    file_response = requests.get(item["download_url"])
                    if file_response.status_code == 200:
                        repo_data[item_path] = file_response.text
                    else:
                        repo_data[item_path] = "Error fetching file"
                
                elif item["type"] == "dir":
                    # Recursive call for nested directories
                    sub_repo_data = get_files(item["url"], path_prefix=item_path + "/")
                    repo_data.update(sub_repo_data)
            
            return repo_data
        else:
            print(f"Failed to fetch repository contents. Status Code: {response.status_code}")
            return {}

    # Fetch all files recursively
    repo_files = get_files(base_api_url)
    
    # Update JSON file: Store under username -> repo -> files
    if owner not in existing_data:
        existing_data[owner] = {}  # Create a new dictionary for the user if not present

    existing_data[owner][repo] = repo_files  # Store repo data under username

    # Save updated data back to JSON
    with open(json_filename, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"Repository file contents updated in {json_filename}")
