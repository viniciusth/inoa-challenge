from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserCreationForm, EditUserForm, TrackAssetForm, RemoveTrackedAssetForm
from .forms import GraphPeriodForm

import pandas as pd
import yfinance as yf
import plotly.offline as opy
from pathlib import Path
import os
# Create your views here.

def home_view(request, *args, **kwargs):
  return render(request, "home.html", {})

def register_view(request, *args, **kwargs):
  form = UserCreationForm(request.POST)
  if form.is_valid():
    form.save()
    return redirect('login')
  else:
    form = UserCreationForm()
  return render(request, "register.html", {'form' : form})

def edit_user_view(request, *args, **kwargs):
  form = EditUserForm(data=request.POST, instance = request.user)
  if form.is_valid():
    form.save()
    return redirect('profile')
  return render(request, "edit_user.html", {'form' : form})

def change_password_view(request, *args, **kwargs):
  form = PasswordChangeForm(data = request.POST, user = request.user)
  if form.is_valid():
    form.save()
    return redirect('login')
  return render(request, "change_password.html", {'form' : form})

def profile_view(request, *args, **kwargs):
  return render(request, "profile.html", {})

def login_view(request, *args, **kwargs):
  form = AuthenticationForm(data=request.POST)
  if form.is_valid():
    login(request, form.get_user())
    return redirect('profile')
  else:
    form = AuthenticationForm()
  return render(request, "login.html", {'form' : form})

def logout_view(request, *args, **kwargs):
  logout(request)
  return render(request, "logged_out.html", {})


def assets_view(request, *args, **kwargs):
  assets = User.objects.get(id = request.user.id).asset_set.all()
  return render(request, "assets.html", {'assets' : assets})

def asset_add_view(request, *args, **kwargs):
  form = TrackAssetForm(data = request.POST)
  if form.is_valid():
    form.save(id = request.user.id)
    return redirect('assets')
  return render(request, "asset_add.html", {'form' : form})

def asset_remove_view(request, *args, **kwargs):
  form = RemoveTrackedAssetForm(data = request.POST, id = request.user.id)
  if form.is_valid():
    form.delete()
    return redirect('assets')
  return render(request, "asset_remove.html", {'form' : form})

def all_assets_view(request, *args, **kwargs):
  pt = Path(__file__).resolve().parent
  pt = os.path.join(pt, 'data')
  pt = os.path.join(pt, 'condensed.csv')
  df = pd.read_csv(pt)
  assets = df['tickers'].tolist()
  assets.sort()
  return render(request, "all_assets.html", {'assets' : assets})





def generate_graph(*args, **kwargs):
  tckr = kwargs['ticker']
  tckr += '.SA'
  ticker = yf.Ticker(tckr)
  hist = ticker.history()
  inter = { "1d":"1m", "5d":"1m", "1mo":"5m"}
  if inter.get(kwargs['period']) != None:
    hist = ticker.history(period=kwargs['period'], interval=inter[kwargs['period']])
  else:
    hist = ticker.history(period=kwargs['period'])
  pd.options.plotting.backend = "plotly"
  df = pd.DataFrame(hist)
  df = df['Open']
  fig = df.plot()
  fig.update_xaxes(title='Date / Time')
  fig.update_yaxes(title='Price')
  fig.update_layout(showlegend=False)
  return (ticker, opy.plot(fig, auto_open=False, output_type='div'))


def period_label(s):
  if s.endswith('d'):
    s = s[:-1] + (' day' if s[0] == '1' else ' days')
  elif s.endswith('mo'):
    s = s[:-2] + (' month' if s[0] == '1' else ' months')
  elif s.endswith('y'):
    s = s[:-1] + (' year' if s[0] == '1' else ' years')
  else:
    s = "All data"
  return s

def some_asset_view(request, *args, **kwargs):
  form = GraphPeriodForm(data = request.POST)
  kwargs['form'] = form
  if form.is_valid():
    kwargs['period'] = form.cleaned_data['period']
    if kwargs['period'] == "":
      kwargs['period'] = "1d"
    (tckr, graph) = generate_graph(*args, **kwargs)
    kwargs['graph'] = graph
    kwargs['period'] = period_label(kwargs['period'])
    kwargs['yf'] = tckr
  return render(request, "some_asset.html", kwargs)