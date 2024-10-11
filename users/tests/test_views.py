from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpPageTests(TestCase):
    def setUp(self) -> None:
        self.name = 'test user'
        self.email = 'testuser@email.com'
        self.bio = 'test user bio'
        self.password = 'fake12345'

    def test_signup_page_view(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('users:signup'), data={
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'password1': self.password,
            'password2': self.password
        })

        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertNotEqual(users[0].password, self.password)