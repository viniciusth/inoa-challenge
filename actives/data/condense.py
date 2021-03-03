import pandas as pd
import os

files = os.listdir('.')
files.remove('condense.py')
files.remove('test_data.py')
tickers = set()
for f in files:
    df = pd.read_csv(f, sep=';')
    tickers.update(set(df['TckrSymb'].tolist()))

df = pd.DataFrame({'tickers' : list(tickers)})

df.to_csv('condensed.csv', index=False)