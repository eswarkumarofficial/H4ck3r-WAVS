from datetime import datetime
import pyfiglet
import requests
from bs4 import BeautifulSoup

ascii_banner = pyfiglet.figlet_format("H4ck3r - wavs")
print(ascii_banner)
print("                                                  "   + "by Eswar H4ck3r" + "\n")

print("-" * 60)
print(str(datetime.now()))
print("-" * 60)

print("\n<<<<<<<<<< Tester >>>>>>>>>>\n")

def create_txt_header(report):
    report.write("H4ck3r - wavs Security Scan Report\n")
    report.write("-" * 60 + "\n")
    report.write(f"Scan Date and Time: {datetime.now()}\n")
    report.write("-" * 60 + "\n\n")

def add_to_txt_report(report, message):
    report.write(message + "\n\n")  # Add an extra line between each message

def highlight(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def highlight_vulnerability(name):
    return highlight(name, "93")  # Yellow color code

def highlight_payload(payload):
    return highlight(payload, "92")  # Green color code

def scan_for_sql_injection(target_url, report):
    print(f"Scanning for SQL injection in {target_url}")
    injection_strings = ["'", '"', " OR 1=1 --", " OR 'a'='a", "' OR 1=1 --", "\" OR 1=1 --"]
    for injection in injection_strings:
        payload = target_url + injection
        print(f"Trying payload: {payload}")
        response = requests.get(payload)
        if "error" in response.text.lower():
            message = (
                f"{highlight_vulnerability('SQL Injection')} vulnerability found: "
                f"{highlight_payload(payload)}"
            )
            print(message)
            add_to_txt_report(report, message)

def scan_for_xss(target_url, report):
    print(f"Scanning for XSS in {target_url}")
    payload = '<script>alert("XSS")</script>'
    response = requests.get(target_url + payload)
    if payload in response.text:
        message = (
            f"{highlight_vulnerability('XSS')} vulnerability found: "
            f"{highlight_payload(payload)}"
        )
        print(message)
        add_to_txt_report(report, message)

def scan_for_directory_traversal(target_url, report):
    print(f"Scanning for Directory Traversal in {target_url}")
    payload = "../../../../etc/passwd"
    response = requests.get(target_url + payload)
    if "root:x" in response.text:
        message = (
            f"{highlight_vulnerability('Directory Traversal')} vulnerability detected! "
            f"{highlight_payload(payload)}"
        )
        print(message)
        add_to_txt_report(report, message)

def scan_for_information_disclosure(target_url, report):
    print(f"Scanning for Information Disclosure in {target_url}")
    response = requests.get(target_url)
    if response.status_code == 200:
        # Check if the response contains sensitive information
        if "password" in response.text.lower() or "private key" in response.text.lower():
            message = (
                f"{highlight_vulnerability('Information Disclosure')} vulnerability found: "
                f"{highlight_payload(target_url)}"
            )
            print(message)
            add_to_txt_report(report, message)

def scan_web_application(target_url, report):
    print(f"Scanning web application at {target_url}")
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        action = form.get("action")
        if action:
            form_url = target_url + action
            scan_for_sql_injection(form_url, report)
            scan_for_xss(form_url, report)
            scan_for_directory_traversal(form_url, report)
            scan_for_information_disclosure(form_url, report)

if __name__ == "__main__":
    try:
        target_url = input("Enter URL to Test: ")
        # Use the URL to create the output file name
        txt_report_path = f"{target_url.replace('http://', '').replace('https://', '').replace('/', '_')}_Security-Report.txt"

        with open(txt_report_path, "w") as txt_report:
            create_txt_header(txt_report)
            scan_web_application(target_url, txt_report)

        print("\nSecurity scan completed.")
        print(f"Report saved to: {txt_report_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
