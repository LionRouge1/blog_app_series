from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpPageTests(TestCase):
  def setUp(self) -> None:
    self.full_name = 'test user'
    self.email = 'testuser@email.com'
    self.bio = 'test user bio'
    self.password = 'fake12345'

  def test_signup_page_view(self):
    """The Signup url should render the 'registration/signup.html' template"""
    response = self.client.get(reverse('users:signup'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, template_name='registration/signup.html')

  def test_signup_correct_data(self):
    """User should be saved when a correct data is provided"""
    response = self.client.post(reverse('users:signup'), data={
      'full_name': self.full_name,
      'email': self.email,
      'bio': self.bio,
      'password1': self.password,
      'password2': self.password
    })
    
    self.assertRedirects(response, reverse('home'))
    users = User.objects.all()
    self.assertEqual(users.count(), 1)
    self.assertNotEqual(users[0].password, self.password)

  def test_signup_fake_data(self):
    """User shouldn't be save we missing email field"""
    response = self.client.post(reverse('users:signup'), data={
      'full_name': self.full_name,
      'email': '',
      'bio': self.bio,
      'password1': self.password,
      'password2': self.password
    })
    
    self.assertEqual(response.status_code, 200)
    users = User.objects.all()
    self.assertEqual(users.count(), 0)