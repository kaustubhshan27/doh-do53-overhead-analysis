#!/bin/python3

import csv
import numpy as np

CLOUDFLARE_CSV_FILE_PATH = '../../results/do53/cloudflare/do53_cloudflare_test_db.csv'
GOOGLE_CSV_FILE_PATH = '../../results/do53/google/do53_google_test_db.csv'

result_csv = [CLOUDFLARE_CSV_FILE_PATH, GOOGLE_CSV_FILE_PATH]

def calculate_stats(list):
    min_val = np.min(list)
    max_val = np.max(list)
    median_val = np.median(list)
    percentile_25 = np.percentile(list, 25)  # 25th percentile
    percentile_75 = np.percentile(list, 75)  # 75th percentile

    print(f"Min. = {min_val}, Max. = {max_val}, Median = {median_val}, 25th%'tile = {percentile_25}, 75th%'tile = {percentile_75}")

def results_parser():

    for result_file in result_csv:
        with open(result_file, newline='') as csvfile:
            pkt_capture = csv.reader(csvfile)

            # get the first line in the packet capture - column names
            headers = next(pkt_capture)

            # general stats
            per_query_size = 0
            per_query_size_list = []

            transaction_id = None
            
            for row in pkt_capture:
                # pairs each header with its corresponding field value in the current row
                record = dict(zip(headers, row))
                if record['Info'].split()[2] == 'response':
                    if transaction_id == record['Info'].split()[3]:
                        per_query_size += int(record['Length'])
                        per_query_size_list.append(per_query_size)
                else:
                    per_query_size = int(record['Length'])
                    transaction_id = record['Info'].split()[2]
        
        print("Per Query Size Stats:")
        calculate_stats(per_query_size_list)

results_parser()
