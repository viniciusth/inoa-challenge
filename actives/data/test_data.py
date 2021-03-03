import pandas as pd
from urllib.request import Request, urlopen

def verify_ticker(ticker):
    url = "https://finance.yahoo.com/quote/{}".format(ticker)
    with urlopen(Request(url)) as response:
        nurl = response.url
        return nurl.endswith('/quote/{}'.format(ticker))
    return False


df = pd.read_csv('condensed.csv')
tickers = df['tickers'].tolist()
total = len(tickers)
at = int(0)
for t in tickers:
    tn = t
    if not tn.endswith('.SA'):
        tn += '.SA'
    at+=1
    print("                                     ", end='\r')
    print("Currently at ticker {}, {}/{}".format(tn, at, total), end='\r')
    if not verify_ticker(tn):
        print("Invalid Ticker - {}".format(tn))
        exit()
print("                                  ", end='\r')
print("All tickers are valid.")
