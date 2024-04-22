import pandas as pd
import numpy as np

df = pd.read_csv(r"Op-cloudflare-radar-domains-top-10000-20240325-20240401.csv")
op = []

for index, row in df.iterrows():
    op.append(row['DNS'])
    #print(row['DNS'])
    #print(row['embeddedDomains'])
    
    if row['embeddedDomains'] not in ["TBD", "Failed to fetch HTML.", np.NaN]:
        for domain in str(row['embeddedDomains']).split(', '):
            op.append(domain)
        pass

opDf = pd.DataFrame(op)
opDf.columns = ['ExtendedDomains']
opDf.to_csv(r"Extended-cloudflare-radar-domains-top-10000-20240325-20240401.csv", index=False, header=False)
