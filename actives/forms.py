from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Active

class UserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True, label='Email')
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user


class EditUser(forms.ModelForm):
	#username = forms.CharField(required=True, widget=forms.TextInput(), label = 'Username')
	email = forms.EmailField(required=True, widget=forms.EmailInput(), label='Email')
	first_name = forms.CharField(required=False, widget=forms.TextInput(), label = "First Name")
	last_name = forms.CharField(required=False, widget=forms.TextInput(), label = "Last Name")
	class Meta:
		model = User
		fields = [ "email", "first_name", "last_name"]

	def save(self, commit=True):
		user = super(EditUser, self).save(commit=False)
		if commit:
			user.save()
		return user
