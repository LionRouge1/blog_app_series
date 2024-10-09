from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class UserTest(TestCase):

  def setUp(self):
    self.user_test = {
      'full_name': 'Tester',
      'email': 'test@gmail.com',
      'bio': 'Biography of Tester',
      'password': 'user12345',
    }
    self.saved = self.create_user(self.user_test)
  
  def create_user(self, data):
    return User.objects.create_user(**data)

  def test_user_creation(self):
    """User creation is successful when all the required field are fill"""
    self.assertTrue(isinstance(self.saved, User))
    self.assertEqual(str(self.saved), self.user_test['email'])

  def test_required_fields(self):
    """Create a user with a empty email or password should raise an Error"""
    fake_user = {
      'full_name': 'fake',
      'email': '',
      'bio': 'fake bio',
      'password': 'user12345'
    }

    with self.assertRaises(TypeError):
      User.objects.create_user()
    with self.assertRaises(TypeError):
      User.objects.create_user(email='tester1@gmail.com')
    with self.assertRaises(ValueError) as context:
      self.create_user(fake_user)
    self.assertEqual(str(context.exception), "The Email must be set")

  def test_password_encripted(self):
    """Saved password in the database should be different from from provided password"""
    self.assertNotEqual(self.saved.password, self.user_test['password'])

  def test_creation_superuser(self):
    super_user = User.objects.create_superuser(email='superuser@gmail.com', password='super12345', bio='User admin')
    self.assertTrue(super_user.is_superuser)