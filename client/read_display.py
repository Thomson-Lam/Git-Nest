import json

def read_and_display_json(json_filename):
    """
    Reads a JSON file and prints its contents in a structured format.
    
    Args:
        json_filename (str): Path to the JSON file.
        
    Returns:
        dict: Parsed JSON content.
    """
    try:
        with open(json_filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Print formatted JSON structure
        print(json.dumps(data, indent=4))

        return data  # Return parsed JSON data
    except FileNotFoundError:
        print(f"Error: The file '{json_filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON. Check the file format.")

# Example Usage
json_data = read_and_display_json("github_file_contents.json")
