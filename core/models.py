from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):


    user = models.OneToOneField(User)
    homepage = models.URLField()


    def __unicode__(self):
        return self.user.username

class TimeStampMixin(models.Model):

    date_added = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Image(TimeStampMixin):

    title = models.TextField()
    author = models.ForeignKey(User)
    path = models.ImageField(upload_to="images")
    thumb_path = models.ImageField(upload_to="thumbnails")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("date_added",)
        verbose_name = "Image"
        verbose_name_plural = "Images"






    

    

