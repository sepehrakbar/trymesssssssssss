import os
import requests

# --- Configuration ---
MOD_COUNT = 40
MINECRAFT_VERSION = "1.21"
MOD_LOADER = "fabric"
MODS_DIR = "mods"
# -------------------

def get_popular_mods():
    """Fetches a list of popular mods from the Modrinth API."""
    print("Fetching list of popular mods...")
    search_url = "https://api.modrinth.com/v2/search"
    params = {
        'limit': MOD_COUNT,
        'index': 'downloads',
        'facets': f'[["categories:{MOD_LOADER}"], ["versions:{MINECRAFT_VERSION}"]]'
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['hits']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod list: {e}")
        return []

def get_mod_version_file(project_id):
    """Finds the correct version file for a given mod project ID."""
    version_url = f"https://api.modrinth.com/v2/project/{project_id}/version"
    params = {
        'loaders': f'["{MOD_LOADER}"]',
        'game_versions': f'["{MINECRAFT_VERSION}"]'
    }
    try:
        response = requests.get(version_url, params=params)
        response.raise_for_status()
        versions = response.json()
        if versions:
            # The first version in the list is the newest compatible one
            # The first file in that version is usually the main mod file
            return versions[0]['files'][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching version for project {project_id}: {e}")
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
        print(f"Successfully saved to {path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

def main():
    """Main function to run the mod downloader."""
    # Create the mods directory if it doesn't exist
    if not os.path.exists(MODS_DIR):
        print(f"Creating directory: '{MODS_DIR}'")
        os.makedirs(MODS_DIR)

    mods_to_download = get_popular_mods()

    if not mods_to_download:
        print("Could not retrieve any mods. Exiting.")
        return

    for mod in mods_to_download:
        print("-" * 20)
        print(f"Processing: {mod['title']}")
        
        file_info = get_mod_version_file(mod['project_id'])
        
        if file_info:
            download_file(file_info['url'], MODS_DIR, file_info['filename'])
        else:
            print(f"Could not find a compatible version for {mod['title']}")

    print("-" * 20)
    print("\nDownload process finished.")
    print(f"You can find your mods in the '{MODS_DIR}' folder.")


if __name__ == "__main__":
    main()
