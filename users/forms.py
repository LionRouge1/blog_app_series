from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django import forms
User = get_user_model()
import re

class CustomUserCreationForm(UserCreationForm):
  """
  Set the password fields to the default messages
  """
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

  class Meta:
    model = CustomUser
    fields = ('full_name', 'email', 'bio',)

  def clean_full_name(self):
    full_name = self.cleaned_data.get('full_name')
    regex = r"^[a-zA-Z]{2,}(?:\s[a-zA-Z]{2,}(?:-[a-zA-Z]{2,})*)+$"
    if not re.match(regex, full_name):
      raise forms.ValidationError("Enter a first and last name.")
    return full_name
  
  def clean_email(self):  
    email = self.cleaned_data.get('email') 
    user = User.objects.filter(email=email)
    if user.exists():  
      raise forms.ValidationError("Email Already Exist")  
    return email
  
  def clean_bio(self):
    bio = self.cleaned_data.get('bio')
    if not len(bio) >= 4:
      raise forms.ValidationError("The bio must be at least 4 characters long. Please provide more details.")
    return bio

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ('full_name', 'photo', 'bio',)