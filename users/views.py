from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import get_user_model, views
User = get_user_model()

class SignUpView(CreateView):
  form_class = CustomUserCreationForm
  redirect_authenticated_user = True
  model = User
  success_url = reverse_lazy('users:login')
  template_name = 'registration/signup.html'
  
  # def dispatch(self, request, *args, **kwargs):
  #   # Check if user is already authenticated
  #   if request.user.is_authenticated:
  #     # Redirect the user to the homepage or any other page if logged in
  #     return redirect(f'{settings.LOGIN_REDIRECT_URL}')  # Replace 'home' with your desired URL name
  #   return super().dispatch(request, *args, **kwargs)
  
class CustomLoginView(views.LoginView):
  form_class = LoginForm
  redirect_authenticated_user = True
  authentication_form = LoginForm
  template_name = 'registration/login.html'
  
  def form_valid(self, form):
    remember_me = form.cleaned_data.get('remember_me')
    
    if not remember_me:
      # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
      self.request.session.set_expiry(0)

      # Set session as modified to force data updates/cookie to be saved.
      self.request.session.modified = True
    return super(CustomLoginView, self).form_valid(form)