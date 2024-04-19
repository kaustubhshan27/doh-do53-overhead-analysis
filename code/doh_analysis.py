#!/bin/python3

import csv
import dns.query
import dns.message
import httpx

# Define the DoH endpoints for Google and Cloudflare
GOOGLE_DNS_HTTPS = 'https://dns.google/dns-query'               # https://developers.google.com/speed/public-dns/docs/doh
CLOUDFLARE_DNS_HTTPS = 'https://cloudflare-dns.com/dns-query'   # https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/

# CSV file path
CSV_FILE_PATH = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/top-domains-db/test_domains.csv'

def resolve_doh(dns_service_url, session=None):
    with open(CSV_FILE_PATH, newline='') as csvfile:
        domain_reader = csv.reader(csvfile)
        for row in domain_reader:
            domain = row[0].strip()
            # Creates a DNS query message
            dns_message = dns.message.make_query(domain, dns.rdatatype.NS)
            # Sends the DNS query message over HTTPS, returns the response from the DoH server
            response = dns.query.https(dns_message, dns_service_url, session=session)
            print(f"Domain: {domain}, DNS Service URL: {dns_service_url}, Response: {response}")

def main():
    # Without persistent connections
    print("\nWithout persistent connections:")
    print("Resolving with Google DNS...")
    resolve_doh(GOOGLE_DNS_HTTPS)
    print("Resolving with Cloudflare DNS...")
    resolve_doh(CLOUDFLARE_DNS_HTTPS)

    # Using persistent connections
    print("Using persistent connections:")
    with httpx.Client() as client:
        #print("Resolving with Google DNS...")
        #resolve_doh(GOOGLE_DNS_HTTPS, session=client)
        print("Resolving with Cloudflare DNS...")
        resolve_doh(CLOUDFLARE_DNS_HTTPS, session=client)

if __name__ == "__main__":
    main()
