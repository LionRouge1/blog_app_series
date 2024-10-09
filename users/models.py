from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from PIL import Image
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
  full_name = models.CharField(_('full name'), blank=False, null=False, max_length=200)
  email = models.EmailField(_('email address'), unique=True, max_length=200)
  photo = models.ImageField(upload_to='profiles', blank=True, null=True, verbose_name='Photo')
  bio = models.TextField(blank=True, null=True, verbose_name='Biography')
  posts_counter = models.PositiveIntegerField(default=0, null=False, verbose_name='Posts Counter')
  updated_at = models.DateTimeField(auto_now=True)
  created_at =  models.DateTimeField(auto_now_add=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def has_perm(self, perm, obj=None):
    return True

  def save(self, *args, **kwargs):
    """
    Overwrite the default method save() to resize the profile picture
    before save using Pillow.
    """
    super().save()
    
    if self.photo:
      img = Image.open(self.photo.path)

      if img.height > 80 or img.width > 80:
        img_size = (80, 80)
        img.thumbnail(img_size)
        img.save(self.photo.path)

  class Meta:
    """
    Set the table name to follow our ERD
    """
    db_table = 'users'
  
  def __str__(self):
    return self.email