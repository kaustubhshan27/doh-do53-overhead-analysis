#!/bin/python3

import csv
import dns.resolver
import sys

# Path to your CSV file
CSV_FILE_PATH = 'top-domains-db/test_domains.csv'

# DNS servers
GOOGLE_DNS = '2001:4860:4860::8888' #'8.8.8.8'
CLOUDFLARE_DNS = '2606:4700:4700::1111' #'1.1.1.1'

def resolve_domains(dns_server):
    # The 'configure' is set to False to avoid using system's default configuration
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_server]

    with open(CSV_FILE_PATH, newline='') as csvfile:
        # To iterate over each row in the file
        domain_reader = csv.reader(csvfile)
        for row in domain_reader:
            # Extracting the first item of each row - domain name
            domain = row[0].strip()
            try:
                # Perform the DNS query
                answer = resolver.resolve(domain, 'NS')
            except Exception as e:
                print(f"Error resolving {domain} using {dns_server}: {e}", file=sys.stderr)

def main():
    # print("Resolving with Google DNS...")
    # resolve_domains(GOOGLE_DNS)
    print("Resolving with Cloudflare DNS...")
    resolve_domains(CLOUDFLARE_DNS)

if __name__ == "__main__":
    main()
