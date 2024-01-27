import requests
import pyfiglet
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style  # Import colorama for color support

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)
print("                                                  " + "by Eswar H4ck3r" + "\n")

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

        print(f"Visited URL: {current_url}")
        print(f"Status Code: {highlight_status_code(response.status_code)}\n")

        if response.status_code != 200:
            # Handle non-OK responses
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith(('http://', 'https://')):
                absolute_url = urljoin(current_url, href)
                if absolute_url not in visited_urls and absolute_url not in queue:
                    queue.append(absolute_url)


def highlight_status_code(status_code):
    if 200 <= status_code < 300:
        return f"{Fore.GREEN}{status_code}{Style.RESET_ALL}"  # Green for success
    elif 300 <= status_code < 400:
        return f"{Fore.BLUE}{status_code}{Style.RESET_ALL}"  # Blue for redirection
    elif 400 <= status_code < 500:
        return f"{Fore.YELLOW}{status_code}{Style.RESET_ALL}"  # Yellow for client errors
    elif 500 <= status_code:
        return f"{Fore.RED}{status_code}{Style.RESET_ALL}"  # Red for server errors
    else:
        return str(status_code)


target_url = input("Enter the Website to Crawl: ")
crawl(target_url)
