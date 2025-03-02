import json

def get_file_content(json_file, repo_owner, repo_name, file_path):
    """
    Reads a JSON file and retrieves the content of a specific file within the 'test' directory.
    
    :param json_file: Path to the JSON file.
    :param repo_owner: The owner of the repository (e.g., "MrPumpkin92").
    :param repo_name: The name of the repository (e.g., "test").
    :param file_path: The specific file path within the repo (e.g., "folder1/anothertest.py").
    :return: File content as a string or an error message.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Navigate through the JSON structure
        if repo_owner in data and repo_name in data[repo_owner]:
            files = data[repo_owner][repo_name]

            if file_path in files:
                return files[file_path]  # Return the content of the specified file
            else:
                return f"Error: File '{file_path}' not found in '{repo_name}'."
        else:
            return f"Error: Repository '{repo_name}' not found under owner '{repo_owner}'."
    
    except FileNotFoundError:
        return "Error: JSON file not found."
    except json.JSONDecodeError:
        return "Error: Failed to parse JSON file."
    

# json_file = "github_file_contents.json"
# repo_owner = "MrPumpkin92"
# repo_name = "test"
# filename = "test.py"

# content = get_file_content(json_file, repo_owner, repo_name, filename)
# print(content)
