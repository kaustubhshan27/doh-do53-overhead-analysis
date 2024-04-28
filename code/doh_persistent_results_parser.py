#!/bin/python3

import csv

# Load the CSV data
google_file_path = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/results/doh-persistent/google/doh-persistent-google-test-db.csv'
cloudflare_file_path = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/results/doh-persistent/cloudflare/doh-persistent-cloudflare-test-db.csv'

result_csv = [google_file_path, cloudflare_file_path]

def results_parser():
    # Initialize min/max trackers
    min_query_size = float('inf')
    max_query_size = float('-inf')
    min_query_pkts = float('inf')
    max_query_pkts = float('-inf')
    dns_request_started = 0

    for result_file in result_csv:
        with open(result_file, newline='') as csvfile:
            pkt_capture = csv.reader(csvfile)

            # Get the first line in the packet capture - column names
            headers = next(pkt_capture)

            per_query_size = 0
            per_query_pkts = 0
            total_capture_size = 0
            total_queries = 0
            total_pkts = 0

            for row in pkt_capture:
                record = dict(zip(headers, row))
                if "[RST," in record['Info'].split() or "[FIN," in record['Info'].split():
                    # calculate stats for the last DNS conversation
                    total_capture_size += per_query_size
                    min_query_size = min(min_query_size, per_query_size)
                    max_query_size = max(max_query_size, per_query_size)
                    min_query_pkts = min(min_query_pkts, per_query_pkts)
                    max_query_pkts = max(max_query_pkts, per_query_pkts)
                    break
                elif "query" in record['Info'].split() and "response" not in record['Info'].split():
                    dns_request_started = 1
                    if per_query_size != 0 and per_query_pkts != 0:
                        # new DNS conversation about to start, calculate stats for the last conversation
                        total_capture_size += per_query_size
                        min_query_size = min(min_query_size, per_query_size)
                        max_query_size = max(max_query_size, per_query_size)
                        min_query_pkts = min(min_query_pkts, per_query_pkts)
                        max_query_pkts = max(max_query_pkts, per_query_pkts)
                    per_query_size = int(record['Length'])
                    per_query_pkts = 1
                    total_queries += 1
                    total_pkts += 1
                else:   
                    if dns_request_started == 1:
                        per_query_size += int(record['Length'])
                        per_query_pkts += 1
                        total_pkts += 1
        
        avg_query_size = total_capture_size / total_queries
        avg_pkts_per_query = total_pkts / total_queries

        print(f"Min. Query Size = {min_query_size}, Max. Query Size = {max_query_size}, Avg. Query Size = {avg_query_size}, Min. Pkts = {min_query_pkts}, Max. Pkts = {max_query_pkts}, Avg. Pkts = {avg_pkts_per_query}")
                    
results_parser()
