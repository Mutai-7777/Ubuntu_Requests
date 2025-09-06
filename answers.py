import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extract filename from URL or generate one if missing"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def get_file_hash(content):
    """Generate hash of file content to detect duplicates"""
    return hashlib.md5(content).hexdigest()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get URLs from user (multiple, separated by spaces)
    urls = input("Please enter one or more image URLs (separate by spaces): ").split()

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    # Track downloaded hashes to prevent duplicates
    downloaded_hashes = set()

    for url in urls:
        try:
            # Fetch the image
            response = requests.get(url, timeout=10, headers={"User-Agent": "UbuntuFetcher/1.0"})
            response.raise_for_status()  # Raise exception for HTTP errors

            # Check important headers before saving
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped {url} — not an image (Content-Type: {content_type})")
                continue

            # Check for duplicates
            file_hash = get_file_hash(response.content)
            if file_hash in downloaded_hashes:
                print(f"✗ Skipped {url} — duplicate image")
                continue
            downloaded_hashes.add(file_hash)

            # Generate filename
            filename = get_filename_from_url(url)
            filepath = os.path.join("Fetched_Images", filename)

            # Save image in binary mode
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
        except Exception as e:
            print(f"✗ Unexpected error for {url}: {e}")

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
