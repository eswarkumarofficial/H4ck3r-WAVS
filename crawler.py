import requests
import pyfiglet as pyfiglet
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)
print("                                                  "   + "by Eswar H4ck3r" + "\n")

print("-" * 60)
print(str(datetime.now()))
print("-" * 60)

print("\n<<<<<<<<<< Crawler >>>>>>>>>>\n")

def crawl(url):
    visited_urls = set()  # To keep track of visited URLs
    queue = [url]  # Queue for URLs to visit

    while queue:
        current_url = queue.pop(0)
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
        except requests.exceptions.RequestException:
            # Handle any request errors
            continue

        if response.status_code != 200:
            # Handle non-OK responses
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Process the current URL here...
        print("Visited URL: " + current_url + "\n")

        # Find and enqueue new URLs to visit
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith(('http://', 'https://')):
                absolute_url = urljoin(current_url, href)
                if absolute_url not in visited_urls and absolute_url not in queue:
                    queue.append(absolute_url)


# Example usage
target_url = input("Enter the Website to Crawl: ")
crawl(target_url)
