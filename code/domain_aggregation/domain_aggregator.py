import pandas as pd
import numpy as np
import requests, re
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException, UnexpectedAlertPresentException, InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_https(domain):
    try:
        response = requests.head(f"https://{domain}", timeout=5)
        if response.status_code == 200:
            return True
        response.raise_for_status()
    except requests.RequestException:
        return False

#filename = "cloudflare-radar-domains-top-10000-20240325-20240401.csv"
filename = "cloudflare-radar-domains-top-100000-20240325-20240401.csv"
#filename = "test_domains.csv"
df = pd.read_csv(rf"Checkpoint-{filename}", header=None)
df.columns = ['DNS', 'embeddedDomains']

bar = IncrementalBar('Fetching embedded domains:', max = len(df[(df['embeddedDomains'] == "TBD")].index))

"""
print(df[(df['embeddedDomains'] == "TBD")].index.to_list()[0])
print(df[(df['embeddedDomains'] == "TBD")])
print(df[(df['embeddedDomains'] == "TBD")].index.to_list()[-1])
"""

# Set up Firefox options
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in background without opening a browser window

# Initialize the WebDriver
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

op = []

"""
df['embeddedDomains'] = pd.Series(dtype='object')
df['embeddedDomains'] = "TBD"
"""

try:
    for index, row in df[(df['embeddedDomains'] == "TBD")].iterrows():
        bar.next()
        """op.append(row['DNS'])"""

        # Fetch the page
        protocol = "https" if check_https(row['DNS']) else "http"
        url = f"{protocol}://{row['DNS']}"
        
        # Set page load timeout
        driver.set_page_load_timeout(3)  # Timeout after 10 seconds
        
        try:
            # Attempt to fetch the page
            driver.get(url)
        except TimeoutException:
            #print(f"TimeoutException: The page took too long to load for URL {url}")
            df.at[index, "embeddedDomains"] = "TimeoutException: The page took too long to load"
            continue
        except WebDriverException as e:
            #print(f"WebDriverException: Problem accessing the URL {url}. Error: {e}")
            df.at[index, "embeddedDomains"] = "WebDriverException: Problem accessing the URL"
            continue
        except:
            df.at[index, "embeddedDomains"] = "Problem accessing the URL"
            continue

        # Extract HTML content
        try:
            # Set implicit wait
            driver.implicitly_wait(3)  # Wait up to 5 seconds for elements to be found

            # Use explicit wait to wait for a specific element to be loaded or condition to be met
            wait = WebDriverWait(driver, 3)  # Timeout after 10 seconds
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Example: Wait for the body tag to be loaded

            html_content = driver.page_source
        except UnexpectedAlertPresentException:
            df.at[index, "embeddedDomains"] = "UnexpectedAlertPresentException: Problem extracting the HTML content"
            continue
        except InvalidArgumentException:
            df.at[index, "embeddedDomains"] = "InvalidArgumentException: Problem extracting the HTML content"
            continue
        except:
            df.at[index, "embeddedDomains"] = "Problem extracting the HTML content"
            continue

        # Process or store HTML code as needed
        url_pattern = re.compile(r'href="(https?://[^"]+)"')

        # Parse HTML code with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all <a> tags containing URLs
        links = soup.find_all('a')

        # Extract URLs from <a> tags
        urls = [link.get('href') for link in links]

        # Filter and extract domains from URLs
        embeddedDomains = [re.match(r'https?://([^/]+)', e_url).group(1) for e_url in urls if e_url is not None and re.match(r'https?://([^/]+)', e_url)]

        df.at[index, "embeddedDomains"] = ', '.join(embeddedDomains)

        # extracted domains
        """for domain in embeddedDomains:
            op.append(domain)"""
        
        df.to_csv(rf"Checkpoint-{filename}", index=False, header=False)
finally:
    # Close the browser
    driver.quit()

bar.finish()

for index, row in df.iterrows():
    op.append(row['DNS'])
    #print(row['DNS'])
    #print(row['embeddedDomains'])

    errorLogs = ["TimeoutException: The page took too long to load",
                 "WebDriverException: Problem accessing the URL",
                 "Problem accessing the URL",
                 "UnexpectedAlertPresentException: Problem extracting the HTML content",
                 "InvalidArgumentException: Problem extracting the HTML content",
                 "Problem extracting the HTML content",
                 "TBD",
                 np.NaN]
    
    if row['embeddedDomains'] not in errorLogs:
        for domain in str(row['embeddedDomains']).split(', '):
            op.append(domain)
        pass

pd.DataFrame(op).to_csv(rf"Extended-{filename}", index=False, header=False)
