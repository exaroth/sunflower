from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, AddBorder, SmartResize
from imagekit import ImageSpec, register
from imagekit.utils import get_field_info
from django.forms.models import model_to_dict
from south.modelsinspector import add_introspection_rules


add_introspection_rules([], [r"core.\thumb.\ImageSpecField"])

# Create your models here.

class ImageThumbnail(ImageSpec):

    format = "JPEG"
    options = {"quality": 80}
    cache_to="thumbnails"

    @property
    def processors(self):
        model, field = get_field_info(self.source)
        return [ResizeToFit(400)]

register.generator("core:image:image_thumbnail", ImageThumbnail)


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name="profile")
    homepage = models.TextField(blank=True)
    avatar = ProcessedImageField(upload_to="avatars",
                                 blank=True,
                                 processors=[SmartResize(100, 100)],
                                 format="JPEG",
                                 options={"quality": 80})

    def __unicode__(self):
        return self.user.username

class TimeStampMixin(models.Model):

    date_added = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomQuerySetManager(models.Manager):
    """A re-usable Manager to access a custom QuerySet"""
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return self.model.QuerySet(self.model)

class Image(TimeStampMixin):

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name="images")
    img = models.ImageField(upload_to="images")
    thumb = ImageSpecField(source="img",
                           id="core:image:image_thumbnail"
                          )
    objects = CustomQuerySetManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("image_details", kwargs={"pk": self.pk})

    def _to_dict(self):
        # Convert item to dictionary
        return dict(
            title = self.title,
            description = self.description or None,
            author = self.author.username,
            img = self.img.url,
            thumb = self.thumb.url,
            date = self.date_added.strftime("%c")
        )

    class QuerySet(QuerySet):

        def queryset_to_list(self):
            # Return list of items containing
            # dicts of items ( for json serialization )
            result = list()
            for item in self:
                result.append(item._to_dict())
            return result

    class Meta:
        ordering = ("-date_added",)
        verbose_name = "Image"
        verbose_name_plural = "Images"

class Category(TimeStampMixin):

    name = models.CharField(max_length=40,
                            help_text="Category name",
                           )
    images = models.ManyToManyField(Image)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
