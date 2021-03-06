from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from .models import Asset

from urllib.request import Request, urlopen

class UserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True, label='Email')
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]
  def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
      user.save()
    return user


class EditUserForm(forms.ModelForm):
  email = forms.EmailField(required=True, widget=forms.EmailInput(), label='Email')
  first_name = forms.CharField(required=False, widget=forms.TextInput(), label = "First Name")
  last_name = forms.CharField(required=False, widget=forms.TextInput(), label = "Last Name")
  class Meta:
    model = User
    fields = [ "email", "first_name", "last_name"]

  def save(self, commit=True):
    user = super(EditUserForm, self).save(commit=False)
    if commit:
      user.save()
    return user


def ticker_exists(ticker):
  url = "https://finance.yahoo.com/quote/{}".format(ticker)
  with urlopen(Request(url)) as response:
    nurl = response.url
    return nurl.endswith('/quote/{}'.format(ticker))
  return False

class TickerField(forms.CharField):

  def ___init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def validate(self, value):
    if not ticker_exists(value):
      raise ValidationError(
        _("Ticker doesn't exist: %(ticker)s"),
        code = 'inexistent_ticker',
        params = {'ticker' : value},
      )
  
  def clean(self, value): # only tickers from B3
    value = super().to_python(value)
    if not value.endswith('.SA'):
      value += '.SA'
    self.validate(value)
    value = value[:-3]
    return value

class TrackAssetForm(forms.ModelForm):
  ticker = TickerField(max_length = 6, required=True, label='Ticker Symbol')
  stop_loss_price = forms.DecimalField(max_digits=20, decimal_places=4, label='Stop Loss Price', required=True)
  stop_limit_price = forms.DecimalField(max_digits=20, decimal_places=4, label='Stop Limit Price', required=True)
  class Meta:
    model = Asset
    fields = ['ticker', 'stop_loss_price', 'stop_limit_price']
  
  def clean(self):
    cleaned_data = super().clean()
    if cleaned_data.get('ticker') != None and cleaned_data['ticker'] != '' and cleaned_data.get('stop_loss_price') > cleaned_data.get('stop_limit_price'):
      raise  ValidationError("The stop loss price can't be bigger than the stop limit price.")  
    return cleaned_data
    
    
  def save(self, commit=True, *args, **kwargs):
    self.cleaned_data = self.clean()
    asset = Asset(
      ticker = self.cleaned_data['ticker'],
      stop_loss_price = self.cleaned_data['stop_loss_price'],
      stop_limit_price = self.cleaned_data['stop_limit_price'],
      user = User.objects.get(id = kwargs['id'])
    )
    if commit:
      asset.save()
      
      
class RemoveTrackedAssetForm(forms.ModelForm):
  asset = forms.ModelChoiceField(queryset=None, required=True)
  class Meta:
    model = Asset
    fields = []
    
  def __init__(self, *args, **kwargs):
    super().__init__(data = kwargs['data'])
    qs = User.objects.get(id = kwargs['id'])
    self.fields['asset'].queryset = qs.asset_set.all()

  def delete(self, *args, **kwargs):
    self.cleaned_data['asset'].delete()
    
valid_periods = [
  ("1d" , "1 day"), 
  ("5d", "5 days"), 
  ("1mo", "1 month"), 
  ("3mo", "3 months"),
  ("6mo", "6 months"), 
  ("1y", "1 year"), 
  ("2y", "2 years"), 
  ("5y", "5 years"), 
  ("10y", "10 years"),
  ("max", "all data")
]
class GraphPeriodForm(forms.Form):
  period = forms.ChoiceField(choices=valid_periods, required=False)