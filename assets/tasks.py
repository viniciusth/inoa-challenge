
from .models import Asset
import yfinance as yf
import pandas as pd
from workers import task
import os
import smtplib
from email.message import EmailMessage

def send_email(recipient, content):
  EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
  EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
  msg = EmailMessage()
  msg['Subject'] = "Asset price warning"
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = recipient
  msg.set_content(content)
  print("Tried sending email to {}, content = {}".format(recipient, content))
  return # following works but i don't want spam
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

@task(schedule=45) # runs the update every 45 seconds
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
    if asset.price <= asset.stop_loss_price:
      send_email(asset.user.email, "Sell the asset: {}, it is below your stop loss price!".format(asset.ticker))
    if asset.price >= asset.stop_limit_price:
      send_email(asset.user.email, "Sell the asset: {}, it is above your stop limit price!".format(asset.ticker))
    asset.save() 