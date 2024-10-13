from django.test import TestCase
from users.forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationFormTest(TestCase):
  def setUp(self):
    self.full_name = 'First Name'
    self.password = 'test12345'
    self.email = 'test@gmail.com'
    self.bio = 'Tester biography'

  def test_email_validation(self):
    """Form should raise error when email is not a valid email"""
    data = {
      'full_name': self.full_name,
      'password1': self.password,
      'password2': self.password,
      'email': 'testegmail.com',
      'bio': self.bio,
    }
    form = CustomUserCreationForm(data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['email'], ["Enter a valid email address."])

  def test_name_validation(self):
    """Form should raise error when the full name is not first and last name"""
    data = {
      'full_name': 'Fake',
      'password1': self.password,
      'password2': self.password,
      'email': 'testegmail',
      'bio': self.bio,
    }
    form = CustomUserCreationForm(data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['full_name'], ["Enter a first and last name."])

  def test_password_confirmation(self):
    """Form should raise error when password do not match"""
    data = {
      'full_name': self.full_name,
      'password1': self.password,
      'password2': 'newowkdkdkd',
      'email': self.email,
      'bio': self.bio,
    }
    form = CustomUserCreationForm(data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])

  def test_bio_validation(self):
    """Form should raise error when the bio is less than 4 characters"""
    data = {
      'full_name': self.full_name,
      'password1': self.password,
      'password2': self.password,
      'email': self.email,
      'bio': 'th',
    }
    form = CustomUserCreationForm(data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['bio'], ["The bio must be at least 4 characters long. Please provide more details."])

  def test_form_validation(self):
    """Form should be valid"""
    data = {
      'full_name': self.full_name,
      'password1': self.password,
      'password2': self.password,
      'email': self.email,
      'bio': self.bio,
    }
    form = CustomUserCreationForm(data)
    self.assertTrue(form.is_valid())
    

class LoginFormTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      full_name= 'Tester User',
      email= 'tester@gmail.com',
      bio= 'new bio for tester',
      password= 'password12345'
    )
    
  def test_valid_credentials(self):
    """
    With valid credentials, the form should be valid
    """
    credentials = {
      'email': 'tester@gmail.com',
      'password': 'password12345',
      'remember_me': False
    }
    
    form = LoginForm(data = credentials)
    self.assertTrue(form.is_valid())
    
  def test_wrong_credentials(self):
    """
    With wrong credentials, the form should raise Invalid email or password error
    """
    credentials = {
      'email': 'tester@gmail.com',
      'password': 'wrongpassword',
      'remember_me': False
    }
    form = LoginForm(data = credentials)
    self.assertIn('Invalid email or password', str(form.errors['__all__']))
    
  def test_credentials_with_empty_email(self):
    """
    Should raise error when the email field is empty
    """
    credentials = {
      'email': '',
      'password': 'wrongpassword',
      'remember_me': False
    }
    form = LoginForm(data = credentials)
    self.assertFalse(form.is_valid())
    self.assertIn('This field is required', str(form.errors['email']))
    
  def test_credentials_with_empty_password(self):
    """
    Should raise error when the password field is empty
    """
    credentials = {
      'email': 'tester@gmail.com',
      'password': '',
      'remember_me': False
    }
    form = LoginForm(data = credentials)
    self.assertFalse(form.is_valid())
    self.assertIn('This field is required', str(form.errors['password']))