from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser
from django import forms
User = get_user_model()
import re

class CustomUserCreationForm(UserCreationForm):
  """
  Set the password fields to the default messages
  """
  full_name = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Enter Full name', 'class': 'form-control'})
  )
  email = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'})
  )
  bio = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Enter author biography', 'class': 'form-control', 'rows': 5})
  )
  password1 = forms.CharField(
    label='Password', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control'})
  )
  password2 = forms.CharField(
    label='Confirm Password', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
  )

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
    
class LoginForm(AuthenticationForm):
  email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control',})
  )
  password = forms.CharField(
    required=True,
    widget=forms.PasswordInput(attrs={
                                'placeholder': 'Password',
                                'class': 'form-control',
                                'data-toggle': 'password',
                                'id': 'password',
                                'name': 'password',
                                })
  )
  remember_me = forms.BooleanField(required=False)
  
  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)
        # Remove username field
    
    if 'username' in self.fields:
      del self.fields['username']
  
  def clean(self):
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')

    # Authenticate using email and password
    if email and password:
      self.user_cache = authenticate(self.request, email=email, password=password)
      if self.user_cache is None:
        raise forms.ValidationError("Invalid email or password")
      else:
        self.confirm_login_allowed(self.user_cache)

    return self.cleaned_data
  
  class Meta:
    model = User
    fields = ('email', 'password', 'remember_me')