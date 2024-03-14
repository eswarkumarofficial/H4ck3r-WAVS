import requests
from datetime import datetime
import pyfiglet
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)
print("                                                  " + "by Eswar H4ck3r" + "\n")

print("-" * 60)
print(str(datetime.now()))
print("-" * 60)

print("\n<<<<<<<<<< Mapper >>>>>>>>>>\n")


def map_web_application(url, save_to_file=False):
    # Send a GET request to the provided URL
    response = requests.get(url)

    # Extract file links from the response
    file_links = extract_file_links(response, base_url=url)

    # Print the discovered file links
    for file_link in file_links:
        print(file_link)

    # Save file links to a text file if requested
    if save_to_file:
        save_links_to_file(file_links, url)


def extract_file_links(response, base_url):
    # Extract file links from the response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    file_links = []

    # Find all anchor tags in the HTML
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href:
            full_url = urljoin(base_url, href)
            if is_file_link(full_url):
                file_links.append(full_url)

    return file_links


def is_file_link(url):
    # Check if the URL points to a file (you can customize this based on your file types)
    file_extensions = ['.pdf', '.doc', '.txt', '.zip', '.jpg', '.png', '.exe', '.php']  # Add more if needed
    _, extension = os.path.splitext(url)
    return extension in file_extensions


def save_links_to_file(links, url):
    # Generate a filename based on the URL
    filename = f"{urlparse(url).hostname}_mapper.txt"
    
    with open(filename, "w") as file:
        file.write("\n".join(links))
    print(f"\nFile links saved to '{filename}'")


# Example usage
target_url = input("Enter the Website to Map: ")

# Set save_to_file to True
save_to_file = True

map_web_application(target_url, save_to_file)
