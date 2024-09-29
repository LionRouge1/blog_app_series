from django.test import TestCase
from django.urls import reverse

class AppTemplateTests(TestCase):
    def test_home_template(self):
        """Render home.html and response status is 200"""
        # Use Django's reverse function to get the URL for the home page
        response = self.client.get(reverse('home'))
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'home.html')
        
        # Optional: Check if certain text is present in the template
        self.assertContains(response, '<h1>This the home page</h1>')

    def test_about_template(self):
        """Render about.html and response status is 200"""
        # Use reverse to get the URL for the about page
        response = self.client.get(reverse('about'))
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'about.html')
        
        # Optional: Check if certain text is present in the template
        self.assertContains(response, '<h1>This the about page</h1>')
