from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserExt(models.Model):

    user = models.OneToOneField(User)
    portrait = models.ImageField(upload_to="profile_images", blank=True)

    class Meta:

        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):

        return "<User Profile: {0}>".format(self.user.username)
