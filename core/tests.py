from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Image

# Create your tests here.


class TestIndex(TestCase):

    def setUp(self):
        self.u = User.objects.create(username="test_user", password="test")

    def create_sample_image(self):

        i = Image.objects.create(title="test image", path="path.jpg", thumb_path="thumb.jpg",author=self.u)

    def test_index_working_properly(self):

        resp = self.client.get(reverse("index"))
        self.assertIn("Index page", resp.content)
        self.assertEquals(200, resp.status_code)

    def test_showing_no_images_when_no_images(self):

        resp = self.client.get(reverse("index"))
        self.assertIn("No pictures uploaded yet", resp.content)

    def test_adding_images(self):

        self.create_sample_image()
        resp = self.client.get(reverse("index"))
        image = resp.context["images"][0]
        self.assertEquals("test image", image.title)
        self.assertNotIn("No pictures uploaded yet", resp.content)










