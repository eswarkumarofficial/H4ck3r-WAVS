import requests
from bs4 import BeautifulSoup


def map_web_application(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)

        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Extract links from the response
        links = extract_links(response)

        # Write the discovered links to the report file
        with open("Mapper.txt", "w") as report:
            for link in links:
                report.write(link + "\n")

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
    except Exception as e:
        print("An error occurred:", e)


def extract_links(response):
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href:
            links.append(href)

    return links


# Example usage
target_url = input("Enter the URL to Map: ")
map_web_application(target_url)
