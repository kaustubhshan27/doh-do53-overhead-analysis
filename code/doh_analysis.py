#!/bin/python3

import csv
import dns.query
import dns.message
import httpx
import time

# Define the DoH endpoints for Google and Cloudflare
GOOGLE_DNS_HTTPS = 'https://dns.google/dns-query'               # https://developers.google.com/speed/public-dns/docs/doh
CLOUDFLARE_DNS_HTTPS = 'https://cloudflare-dns.com/dns-query'   # https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/

# CSV file path
CSV_FILE_PATH = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/top-domains-db/Extended-cloudflare-radar-domains-top-10000-20240325-20240401.csv'

def resolve_doh(dns_service_url, session=None, csv_file_path='path_to_your_csv_file.csv'):
    with open(csv_file_path, newline='') as csvfile:
        domain_reader = csv.reader(csvfile)
        for row in domain_reader:
            domain = row[0].strip()
            response = None  # Initialize response to handle cases where DNS query fails
            # Creates a DNS query message
            try:
                dns_message = dns.message.make_query(domain, dns.rdatatype.NS)
                try:
                    # Sends the DNS query message over HTTPS, returns the response from the DoH server
                    response = dns.query.https(dns_message, dns_service_url, session=session)
                except Exception as e:
                    print(f"Error handling domain {domain}: {e}")
            except Exception as e:
                print(f"Error handling domain {domain}: {e}")
            print(f"Domain: {domain}, DNS Service URL: {dns_service_url}, Response: {response}")
            #time.sleep(0.1)

def main():
    # Without persistent connections
    print("\nWithout persistent connections:")
    print("Resolving with Google DNS...")
    resolve_doh(GOOGLE_DNS_HTTPS)
    print("Resolving with Cloudflare DNS...")
    resolve_doh(CLOUDFLARE_DNS_HTTPS)

    # Using persistent connections
    print("Using persistent connections:")
    with httpx.Client(http2=True) as client:
        print("Resolving with Google DNS...")
        resolve_doh(GOOGLE_DNS_HTTPS, session=client)
        print("Resolving with Cloudflare DNS...")
        resolve_doh(CLOUDFLARE_DNS_HTTPS, session=client)

if __name__ == "__main__":
    main()
