import requests
import dns.resolver
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BANNER = r"""
  _____                    _           
 |  __ \                  | |          
 | |  | | __ _ _ __   __ _| | ___ _ __ 
 | |  | |/ _` | '_ \ / _` | |/ _ \ '__|
 | |__| | (_| | | | | (_| | |  __/ |   
 |_____/ \__,_|_| |_|\__, |_|\___|_|   
                      __/ |            
                     |___/             

Dangling Domain Finder by Raleigh Guevarra
Version: 1.0
"""

def print_banner():
    print(BANNER)

def find_subdomains(domain):
    """Find subdomains from crt.sh"""
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            json_data = response.json()
            for entry in json_data:
                subdomains.add(entry['name_value'])
        except ValueError:
            print("Error parsing JSON from crt.sh")
    return list(subdomains)

def resolve_subdomain(subdomain):
    """Check if a subdomain is active or dangling"""
    try:
        dns.resolver.resolve(subdomain)
        return subdomain, 'Active'
    except dns.resolver.NXDOMAIN:
        return subdomain, 'NXDOMAIN'
    except Exception as e:
        return subdomain, f'Error: {e}'

def print_results(subdomains, title="Results"):
    print("\n" + title)
    print("-" * 70)
    print("| {:<50} | {:<15} |".format("Subdomain", "Status"))
    print("-" * 70)
    for subdomain, status in subdomains:
        for line in subdomain.split('\n'):
            print("| {:<50} | {:<15} |".format(line.strip(), status))
    print("-" * 70)

def check_subdomains(domain):
    """Resolve each subdomain and collect metrics"""
    subdomains = find_subdomains(domain)
    results = []
    total_subdomains = len(subdomains)
    total_active = 0
    total_dangling = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subdomain = {executor.submit(resolve_subdomain, subdomain): subdomain for subdomain in subdomains}
        for future in as_completed(future_to_subdomain):
            subdomain, status = future.result()
            results.append((subdomain, status))
            if status == 'Active':
                total_active += 1
            else:
                total_dangling += 1
                
    end_time = time.time()
    total_time = end_time - start_time
    
    return results, total_time, total_subdomains, total_active, total_dangling

def main():
    """Main function to parse arguments and initiate domain check"""
    parser = argparse.ArgumentParser(description="Dangling Domain Finder")
    parser.add_argument("domain", type=str, help="The target domain.")
    args = parser.parse_args()

    print_banner()
    results, total_time, total_subdomains, total_active, total_dangling = check_subdomains(args.domain)
    
    print_results(results, "Dangling Domain Finder Results")
    
    print("\nSummary Metrics:")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total subdomains: {total_subdomains}")
    print(f"Total active domains: {total_active}")
    print(f"Total dangling domains: {total_dangling}")

if __name__ == "__main__":
    main()