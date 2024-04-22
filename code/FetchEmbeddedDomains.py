import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

#df = pd.read_csv(r"cloudflare-radar-domains-top-10000-20240325-20240401.csv", header=None)
df = pd.read_csv(r"cloudflare-radar-domains-top-100000-20240325-20240401.csv", header=None)
#df = pd.read_csv(r"test_domains.csv", header=None)
df.columns = ['DNS']
df['embeddedDomains'] = pd.Series(dtype='object')
df['embeddedDomains'] = "TBD"
print(df, end='\n\n')

def check_https(domain):
    try:
        response = requests.head(f"https://{domain}", timeout=5)
        if response.status_code == 200:
            return True
        response.raise_for_status()
    except requests.RequestException:
        return False

bar = IncrementalBar('Fetching embedded domains:', max = len(df.index))

for index, row in df.iterrows():
    bar.next()
    try:
        # Make HTTP GET request
        #response = requests.get("https://" + str(row['DNS']))
        protocol = "https" if check_https(row['DNS']) else "http"
        url2 = f"{protocol}://{row['DNS']}"
        response = requests.get(url2, timeout=5)
        
        # Check if request was successful
        if response.status_code == 200:
            # Extract HTML code
            html_code = response.text
            
            # Process or store HTML code as needed
            url_pattern = re.compile(r'href="(https?://[^"]+)"')

            # Parse HTML code with BeautifulSoup
            soup = BeautifulSoup(html_code, 'html.parser')

            # Find all <a> tags containing URLs
            links = soup.find_all('a')

            # Extract URLs from <a> tags
            urls = [link.get('href') for link in links]

            # Filter and extract domains from URLs
            embeddedDomains = [re.match(r'https?://([^/]+)', url).group(1) for url in urls if re.match(r'https?://([^/]+)', url)]

            # extracted domains
            #print(embeddedDomains)
            df.at[index, "embeddedDomains"] = ', '.join(embeddedDomains)
        else:
            #print(f"Failed to retrieve HTML for {row['DNS']}. Status code: {response.status_code}")
            df.at[index, "embeddedDomains"] = "Failed to fetch HTML."
            pass
    
    except Exception as e:
        #print(f"Error occurred while fetching HTML for {domain}: {str(e)}")
        df.at[index, "embeddedDomains"] = "Failed to fetch HTML."
        pass
    df.to_csv(r"op.csv", index=False)

bar.finish()

