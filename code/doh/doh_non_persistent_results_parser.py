#!/bin/python3

import csv
import numpy as np
from collections import defaultdict

CLOUDFLARE_CSV_FILE_PATH = '../../results/doh-non-persistent/cloudflare/doh_non_persistent_cloudflare_test_db.csv'
GOOGLE_CSV_FILE_PATH = '../../results/doh-non-persistent/google/doh_non_persistent_google_test_db.csv'

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
            per_query_pkts = 0
            per_query_pkts_list = []
            
            # http stats
            per_query_http_data_size = 0
            per_query_http_data_size_list = []
            per_query_http_mgmt_size = 0
            per_query_http_mgmt_size_list = []
            per_query_http_headers_size = 0
            per_query_http_headers_size_list = []

            # tcp stats
            per_query_tcp_size = 0
            per_query_tcp_size_list = []

            # tls stats
            per_query_tls_size = 0
            per_query_tls_size_list = []

            for row in pkt_capture:
                record = dict(zip(headers, row))
                if record['TCP Header Length'] != '':
                        per_query_tcp_size += int(record['TCP Header Length'])
                if record['TLS Length'] != '':
                        size_field = record['TLS Length'].split(',')
                        size_field = [int(size) for size in size_field]
                        for size in size_field:
                            per_query_tls_size += size
                if "[SYN]" in record['Info'].split():
                    if per_query_size != 0 and per_query_pkts != 0:
                        # new DNS conversation about to start, calculate stats for the last conversation
                        per_query_size_list.append(per_query_size)
                        per_query_pkts_list.append(per_query_pkts)
                        per_query_http_data_size_list.append(per_query_http_data_size)
                        per_query_http_mgmt_size_list.append(per_query_http_mgmt_size)
                        per_query_http_headers_size_list.append(per_query_http_headers_size)
                        per_query_tcp_size_list.append(per_query_tcp_size)
                        per_query_tls_size_list.append(per_query_tls_size)
                    
                    # initialize stats for the new DNS conversation
                    per_query_size = int(record['Length'])
                    per_query_pkts = 1
                    per_query_http_data_size = 0
                    per_query_http_mgmt_size = 0
                    per_query_http_headers_size = 0
                    per_query_tcp_size = 0
                    per_query_tls_size = 0
                else:
                    per_query_size += int(record['Length'])
                    per_query_pkts += 1
                    if record['Protocol'].split() == ['HTTP2'] or record['Protocol'].split() == ['DoH']:
                        type_field = record['Type'].split(',')
                        size_field = record['HTTP2 Length'].split(',')
                        size_field = [int(size) for size in size_field]
                        type_size_mapping = list(zip(type_field, size_field))
                        for typ, size in type_size_mapping:
                            if typ == 'DATA':
                                per_query_http_data_size += size
                            elif typ == 'HEADERS' or typ == 'CONTINUATION':
                                per_query_http_headers_size += size
                            else:
                                per_query_http_mgmt_size += size

            # calculate stats for the last DNS conversation
            per_query_size_list.append(per_query_size)
            per_query_pkts_list.append(per_query_pkts)
            per_query_http_data_size_list.append(per_query_http_data_size)
            per_query_http_mgmt_size_list.append(per_query_http_mgmt_size)
            per_query_http_headers_size_list.append(per_query_http_headers_size)
            per_query_tcp_size_list.append(per_query_tcp_size)
            per_query_tls_size_list.append(per_query_tls_size)

        print("Per Query Size Stats:")
        calculate_stats(per_query_size_list)

        print("Per Query Packets Stats:")
        calculate_stats(per_query_pkts)

        print("Per Query HTTP Data Size Stats:")
        calculate_stats(per_query_http_data_size)

        print("Per Query HTTP Mgmt Size Stats:")
        calculate_stats(per_query_http_mgmt_size)

        print("Per Query HTTP Headers Size Stats:")
        calculate_stats(per_query_http_headers_size)

        print("Per Query TCP Size Stats:")
        calculate_stats(per_query_tcp_size_list)

        print("Per Query TLS Size Stats:")
        calculate_stats(per_query_tls_size_list)
                    
results_parser()
