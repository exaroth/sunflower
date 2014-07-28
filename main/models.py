from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserExt(models.Model):

    user = models.OneToOneField(User)
    portrait = models.ImageField(upload_to="profile_images", blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):

        return "<User Profile: {0}>".format(self.user.username)


class Image(models.Model):

    title = models.CharField(max_length=144, blank=False, db_index=True)
    description = models.TextField(blank=True)
    uploader = models.ForeignKey(User, null=False)
    path = models.ImageField(upload_to="images")
    thumb_path = models.ImageField(upload_to="thumbs")
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)


    class Meta:

        verbose_name = "Picture"
        verbose_name_plural = "Pictures"
        ordering = ("modified",)


    def __unicode__(self):

        return "<Image: {0}>".format(self.title)

