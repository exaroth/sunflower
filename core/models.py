from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, AddBorder, SmartResize
from imagekit import ImageSpec, register
from imagekit.utils import get_field_info
from django.forms.models import model_to_dict
from south.modelsinspector import add_introspection_rules
from django.core import serializers


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
    homepage = models.URLField(blank=True)
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

class JSONConvertibleManager(models.Manager):
    
    def __init__(self, *args, **kwargs):
        # fields of the model to be displayed
        self.json_fields = None
        return super(JSONConvertibleManager, self).__init__(*args, **kwargs)

    def define_fields(self, fields=None):
        
        """
        Define custom fields to be displayed
        :param fields -- tuple containing name
        of the fields to be added to the query
        """
        self.json_fields = fields 
        return self

    def get_queryset(self):
        instance = super(JSONConvertibleManager, self).get_queryset()
        return self._convert_to_json(instance)

    def _convert_to_json(self, data):
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        kwargs = dict()
        if self.json_fields:
            kwargs["fields"] = self.json_fields
        return json_serializer.serialize(data, indent=4, **kwargs)


class Image(TimeStampMixin):

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name="images")
    img = models.ImageField(upload_to="images")
    thumb = ImageSpecField(source="img",
                           id="core:image:image_thumbnail"
                          )
    objects = models.Manager()
    json_data = JSONConvertibleManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("image_details", kwargs={"pk": self.pk})

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


