import requests
from datetime import datetime
import pyfiglet as pyfiglet
from bs4 import BeautifulSoup

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)
print("                                                  "   + "by Eswar H4ck3r" + "\n")

print("-" * 60)
print(str(datetime.now()))
print("-" * 60)

print("\n<<<<<<<<<< Mapper >>>>>>>>>>\n")

def map_web_application(url):
    # Send a GET request to the provided URL
    response = requests.get(url)

    # Extract links from the response
    links = extract_links(response)

    # Print the discovered links
    for link in links:
        print(link +"\n")


def extract_links(response):
    # Extract links from the response using a library like BeautifulSoup
    # This example uses BeautifulSoup for HTML parsing
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    # Find all anchor tags in the HTML
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href:
            links.append(href)

    return links


# Example usage
target_url = input("Enter the Website to Map : ")
map_web_application(target_url)

