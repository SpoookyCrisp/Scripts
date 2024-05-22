import subprocess
import time

def query_dns(domain):
    try:
        dig_output = subprocess.check_output(["dig", "+short", domain])
        return dig_output.decode().strip().split("\n")
    except subprocess.CalledProcessError:
        return []

def check_stale_entries(input_file):
    stale_entries = []
    with open(input_file, "r") as f:
        for line in f:
            domain = line.strip()
            actual_ips = query_dns(domain)
            if not actual_ips:
                stale_entries.append((domain, "No IP found"))
                print(f"{domain} is stale. No IP found.")
            else:
                print(f"{domain} resolved to {', '.join(actual_ips)}")
            time.sleep(1)  # Add a delay to avoid rate limiting
    return stale_entries

if __name__ == "__main__":
    input_file = "fqdns.txt"  # Replace with your input file
    stale_entries = check_stale_entries(input_file)
    if stale_entries:
        print("\nSummary of stale entries:")
        for domain, status in stale_entries:
            print(f"{domain}: {status}")
    else:
        print("No stale entries found.")