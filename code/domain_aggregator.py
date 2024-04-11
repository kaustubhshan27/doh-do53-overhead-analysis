#!/bin/python3

import dns.resolver
import time

class StubResolver:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.query_log = {}
        self.unique_domains = set()
    
    def resolve_domain(self, domain_name):
        try:
            start_time = time.time()
            answers = self.resolver.resolve(domain_name, 'A')
            elapsed_time = time.time() - start_time

            if domain_name not in self.query_log:
                self.query_log[domain_name] = {'count': 1, 'time': elapsed_time}
            else:
                self.query_log[domain_name]['count'] += 1
                self.query_log[domain_name]['time'] += elapsed_time
            
            # Add to unique domains
            self.unique_domains.add(domain_name)

        except Exception as e:
            print(f"Error resolving {domain_name}: e")
    
    def report(self):
        total_queries = sum(entry['count'] for entry in self.query_log.values())
        print(f"Total DNS Queries Made: {total_queries}")
        print(f"Total Unique Domains Queried: {len(self.unique_domains)}")

if __name__ == "__main__":
    resolver = StubResolver()
    with open('top-domains-db/cloudflare-radar-domains-top-10000-20240325-20240401.csv', 'r') as domain_db:
        for domain in domain_db:
            domain = domain.strip()
            resolver.resolve_domain(domain)
    
    resolver.report()
