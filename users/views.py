from django.views.generic import CreateView
from django.urls import reverse_lazy
from forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpView(CreateView):
  form_class = CustomUserCreationForm
  model = User
  success_url = reverse_lazy('/')
  template_name = 'registration/signup.html'