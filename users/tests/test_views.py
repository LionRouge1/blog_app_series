from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpTests(TestCase):
  def setUp(self):
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
    
    self.assertRedirects(response, reverse('users:login'))
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
    
class LoginTests(TestCase):
  def setUp(self):
    User.objects.create_user(
      full_name= 'Tester User',
      email= 'tester@gmail.com',
      bio= 'new bio for tester',
      password= 'password12345'
    )
    
  def test_login_url(self):
    """User can navigate to the login page"""
    response = self.client.get(reverse('users:login'))
    self.assertEqual(response.status_code, 200)
  
  def test_login_template(self):
    """Login page render the correct template"""
    response = self.client.get(reverse('users:login'))
    self.assertTemplateUsed(response, template_name='registration/login.html')
    self.assertContains(response, '<a class="btn btn-outline-dark text-white" href="/users/sign_up/">Sign Up</a>')

  def test_login_with_valid_credentials(self):
    """User should be log in when enter valid credentials"""
    credentials = {
      'email': 'tester@gmail.com',
      'password': 'password12345',
      'remember_me': False
    }
    
    response = self.client.post(reverse('users:login'), credentials, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertRedirects(response, reverse('home'))
    self.assertTrue(response.context['user'].is_authenticated)
    self.assertContains(response, '<button type="submit" class="btn btn-danger"><i class="bi bi-door-open-fill"></i> Log out</button>')
    
  def test_login_with_wrong_credentials(self):
    """Get error message when enter wrong credentials"""
    credentials = {
      'email': 'tester@gmail.com',
      'password': 'wrongpassword',
      'remember_me': False
    }
    
    response = self.client.post(reverse('users:login'), credentials, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Invalid email or password')
    self.assertFalse(response.context['user'].is_authenticated)