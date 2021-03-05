
from .models import Asset
import yfinance as yf
import pandas as pd
from workers import task

@task(schedule=60)
def update_asset_prices():
  print("Updating all asset prices!")
  qset = Asset.objects.all()
  for asset in qset:
    tckr = asset.ticker + '.SA'
    ticker = yf.Ticker(tckr)
    hist = ticker.history(period="1d", interval="1m")
    df = pd.DataFrame(hist)
    df = df['Open']
    asset.price = df.iloc[-1]
    asset.save()