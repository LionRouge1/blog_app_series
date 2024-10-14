from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import get_user_model, views
User = get_user_model()

class SignUpView(CreateView):
  form_class = CustomUserCreationForm
  model = User
  success_url = reverse_lazy('home')
  template_name = 'registration/signup.html'
  
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