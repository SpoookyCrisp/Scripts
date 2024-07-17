import subprocess
import time
from openpyxl import Workbook
from datetime import datetime
import os


def query_dns(domain):
    try:
        dig_output = subprocess.check_output(["dig", "+short", domain])
        return dig_output.decode().strip().split("\n")
    except subprocess.CalledProcessError:
        return []

def check_stale_entries(input_file):
   # Export results to a XLS
    wb = Workbook()
    ws = wb.active
    ws.title = "DNS Check Results"
    ws.append(["Domain", "Status", "IP Addresses", "Timestamp"])
    # Begin stale entries analysis
    stale_entries = []
    with open(input_file, "r") as f:
        for line in f:
            domain = line.strip()
            actual_ips = query_dns(domain)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not actual_ips:
                status = "Stale (No IP found)"
                stale_entries.append((domain, status))
                print(f"{domain} is stale. No IP found.")
            else:
                status = "Resolved"
                print(f"{domain} resolved to {', '.join(actual_ips)}")
            
            ws.append([domain, status, ", ".join(actual_ips), timestamp])
            time.sleep(1)  # Add a delay to avoid rate limiting
    return stale_entries

# Ask for file to use

def get_input_file():
    while True:
        file_name = input("Enter the name of the input file containing FQDNs: ").strip()
        if os.path.isfile(file_name):
            return file_name
        else:
            print(f"File '{file_name}' not found. Please try again.")

if __name__ == "__main__":
    input_file = get_input_file()  
    stale_entries = check_stale_entries(input_file)
    if stale_entries:
        print("\nSummary of stale entries:")
        for domain, status in stale_entries:
            print(f"{domain}: {status}")
    else:
        print("No stale entries found.")