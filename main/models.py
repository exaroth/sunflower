from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserExt(models.Model):

    user = models.OneToOneField(User)

    portrait = models.ImageField(upload_to="profile_images")
