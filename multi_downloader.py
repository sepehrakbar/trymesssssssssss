import os
import requests

# --- Configuration ---
ITEM_COUNT_PER_CATEGORY = 10
MINECRAFT_VERSION = "1.21"
# Note: 'shader' is the correct category for the API, not 'shaderpack'
CATEGORIES = ['mod', 'shader', 'resourcepack', 'plugin'] 
BASE_DIR = "minecraft_assets"
# -------------------

def get_popular_items(category, count):
    """Fetches a list of popular items for a given category from the Modrinth API."""
    print(f"Fetching list of {count} popular {category}s...")
    search_url = "https://api.modrinth.com/v2/search"
    # Facets are how we filter by category and version
    facets = f'[["project_type:{category}"], ["versions:{MINECRAFT_VERSION}"]]'
    params = {
        'limit': count,
        'index': 'downloads',
        'facets': facets
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        return response.json()['hits']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {category} list: {e}")
        return []

def get_item_version_file(project_id):
    """Finds the correct version file for a given item, preferring Fabric loader if applicable."""
    version_url = f"https://api.modrinth.com/v2/project/{project_id}/version"
    # Prioritize Fabric, but not all assets have loaders (e.g. resource packs)
    params = {
        'loaders': '["fabric"]', 
        'game_versions': f'["{MINECRAFT_VERSION}"]'
    }
    try:
        response = requests.get(version_url, params=params)
        response.raise_for_status()
        versions = response.json()
        if versions:
            return versions[0]['files'][0]
        else:
            # If no Fabric version is found, try again without loader filter
            del params['loaders']
            response = requests.get(version_url, params=params)
            response.raise_for_status()
            versions = response.json()
            if versions:
                return versions[0]['files'][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Could not get version for project {project_id}: {e}")
        return None


def download_file(url, directory, filename):
    """Downloads a file from a URL to a specific directory."""
    path = os.path.join(directory, filename)
    print(f"Downloading {filename}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"  > Saved to {path}")
    except requests.exceptions.RequestException as e:
        print(f"  > Error downloading {filename}: {e}")

def main():
    """Main function to run the multi-downloader."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for category in CATEGORIES:
        # Create a subdirectory for the category
        category_dir = os.path.join(BASE_DIR, f"{category}s") # e.g., 'mods', 'shaders'
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        items_to_download = get_popular_items(category, ITEM_COUNT_PER_CATEGORY)

        if not items_to_download:
            print(f"Could not retrieve any {category}s. Skipping.")
            continue
        
        print(f"--- Starting downloads for {category.capitalize()}s ---")
        for item in items_to_download:
            print("-" * 20)
            print(f"Processing: {item['title']}")
            
            file_info = get_item_version_file(item['project_id'])
            
            if file_info:
                download_file(file_info['url'], category_dir, file_info['filename'])
            else:
                print(f"Could not find a compatible version for {item['title']}")
        print(f"--- Finished downloads for {category.capitalize()}s ---")

    print("\n==================================")
    print("All downloads finished!")
    print(f"You can find your assets in the '{BASE_DIR}' folder, sorted by category.")
    print("==================================")


if __name__ == "__main__":
    main()
