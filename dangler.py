from prettytable import PrettyTable
import argparse
import csv
import requests
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

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
    try:
        dns.resolver.resolve(subdomain)
        return subdomain, 'Active'
    except dns.resolver.NXDOMAIN:
        return subdomain, 'NXDOMAIN'
    except Exception as e:
        return subdomain, f'Error: {e}'

def print_results(subdomains, title="Results"):
    table = PrettyTable()
    table.field_names = ["Subdomain", "Status"]
    for subdomain, status in subdomains:
        table.add_row([subdomain, status])
    print("\n" + title)
    print(table)

def write_results_to_csv(subdomains, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Subdomain", "Status"])
        for subdomain, status in subdomains:
            csvwriter.writerow([subdomain, status])
    print(f"Results saved to {filename}")

def check_subdomains(domain, show_all, output_file):
    subdomains = find_subdomains(domain)
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(resolve_subdomain, subdomain) for subdomain in subdomains]
        for future in as_completed(futures):
            results.append(future.result())

    if show_all:
        print_results(results, "Dangling Domain Finder Results")
    if output_file:
        write_results_to_csv(results, output_file)

    return results

def main():
    parser = argparse.ArgumentParser(description="Dangling Domain Finder")
    parser.add_argument("domain", type=str, help="The target domain.", nargs='?')
    parser.add_argument("-s", "--show", action='store_true', help="Show all discovered subdomains")
    parser.add_argument("-o", "--output", type=str, help="Output results to a CSV file")
    
    print_banner()
    
    args = parser.parse_args()
    if not args.domain:
        parser.print_help()
        sys.exit(1)

    check_subdomains(args.domain, args.show, args.output)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
