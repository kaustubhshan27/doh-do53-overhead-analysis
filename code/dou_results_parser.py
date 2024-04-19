#!/bin/python3

import csv

CLOUDFLARE_CSV_FILE_PATH = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/results/dou/cloudflare/dou_cloudflare_test_db.csv'
GOOGLE_CSV_FILE_PATH = '/home/kaustubh/Documents/VT-Courses/Spring_24/ECE5560-Fundamentals_Of_InfoSec/project/doh-dou-overhead-analysis/results/dou/google/dou_google_test_db.csv'

result_csv = [CLOUDFLARE_CSV_FILE_PATH, GOOGLE_CSV_FILE_PATH]

def results_parser():
    # Initialize min/max trackers
    min_query_size = float('inf')
    max_query_size = float('-inf')

    for result_file in result_csv:
        with open(result_file, newline='') as csvfile:
            pkt_capture = csv.reader(csvfile)

            # Get the first line in the packet capture - column names
            headers = next(pkt_capture)

            per_query_size = 0
            total_capture_size = 0
            total_queries = 0
            transaction_id = None
            
            for row in pkt_capture:
                # Pairs each header with its corresponding field value in the current row
                record = dict(zip(headers, row))
                if record['Info'].split()[2] == 'response':
                    if transaction_id == record['Info'].split()[3]:
                        total_queries += 1
                        per_query_size += int(record['Length'])
                        min_query_size = min(min_query_size, per_query_size)
                        max_query_size = max(max_query_size, per_query_size)
                        total_capture_size += per_query_size
                else:
                    per_query_size = int(record['Length'])
                    transaction_id = record['Info'].split()[2]

            avg_query_size = total_capture_size / total_queries
            
            print(f"Min. Query Size = {min_query_size}, Max. Query Size = {max_query_size}, Avg. Query Size = {avg_query_size}")

results_parser()
