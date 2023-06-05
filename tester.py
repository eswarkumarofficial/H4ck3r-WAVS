from datetime import datetime
import pyfiglet as pyfiglet
import requests
from bs4 import BeautifulSoup

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)

print("-" * 60)
print(str(datetime.now()))
print("-" * 60)

report = open("Report.txt", "w")

# checking for sql injection
def scan_for_sql_injection(target_url):
    injection_strings = ["'", '"', " OR 1=1 --", " OR 'a'='a", "' OR 1=1 --", "\" OR 1=1 --"]
    for injection in injection_strings:
        payload = target_url + injection
        response = requests.get(payload)
        if "error" in response.text.lower():
            report.write(f"\nSQL Injection vulnerability found: {payload}\n")


# checking for xss
def scan_for_xss(target_url):
    payload = '<script>alert("XSS")</script>'
    response = requests.get(target_url + payload)
    if payload in response.text:
        report.write(f"\nXSS vulnerability found: {target_url}\n")


# checking for directory traversal
def scan_for_directory_traversal(target_url):
    payload = "../../../../etc/passwd"
    response = requests.get(target_url + payload)
    if "root:x" in response.text:
        report.write("\nDirectory Traversal vulnerability detected!\n")


# checking for info-disclose
def scan_for_information_disclosure(target_url):
    response = requests.get(target_url)
    if response.status_code == 200:
        # Check if the response contains sensitive information
        if "password" in response.text.lower() or "private key" in response.text.lower():
            report.write(f"\nInformation disclosure vulnerability found: {target_url}\n")


def scan_web_application(target_url):
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        action = form.get("action")
        if action:
            form_url = target_url + action
            scan_for_sql_injection(form_url)
            scan_for_xss(form_url)
            scan_for_directory_traversal(form_url)
            scan_for_information_disclosure(form_url)


if __name__ == "__main__":
    target_url = input("Enter URL to Test: ")
    scan_web_application(target_url)

report.close()
