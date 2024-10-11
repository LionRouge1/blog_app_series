from django.test import TestCase
from users.forms import CustomUserCreationForm

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