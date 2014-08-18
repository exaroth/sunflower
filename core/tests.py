from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
import os

from .models import Image, UserProfile

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
    
    # not working since js is appending images
    # def test_showing_no_images_when_no_images(self):
    #
    #     resp = self.client.get(reverse("index"))
    #     self.assertIn("No pictures uploaded yet", resp.content)

    # def test_adding_images(self):
    #
    #     self.create_sample_image()
    #     resp = self.client.get(reverse("index"))
    #     image = resp.context["images"][0]
    #     self.assertEquals("test image", image.title)
    #     self.assertNotIn("No pictures uploaded yet", resp.content)


class TestAddingUsers(TestCase):

    def setUp(self):
        self.u = User.objects.create(username="test_user", password="test")

    def test_sanity(self):

        resp = self.client.get(reverse("account_create"))
        self.assertEquals(200, resp.status_code )
        self.assertIn("Create account view", resp.content )

    def test_adding_new_user(self):

        resp = self.client.post(reverse("account_create"), dict(
            username = "new_user",
            password = "test",
            password2="test"
        ), follow=True)

        self.assertIn("Index page", resp.content )
        self.assertEquals(200, resp.status_code)

        user = User.objects.filter(username__exact="new_user")
        self.assertTrue(user.exists())

        resp = self.client.post(reverse("account_create"), dict(
            username = "new_user2",
            password = "test",
            password2="test",
        ), follow=True)

        user_data = User.objects.filter(username__exact="new_user2").get()

        # test for duplicates

        resp = self.client.post(reverse("account_create"), dict(
            username = "test_user",
            password = "test",
            password2="test"
        ), follow=True)

        self.assertIn("User with this Username already exists", resp.content)

        # test for password mismatch

        resp = self.client.post(reverse("account_create"), dict(
            username = "new_user",
            password = "test",
            password2="test2"
        ), follow=True)

        self.assertIn("Password Mismatch", resp.content)

    def test_logging_users(self):

        self.client.post(reverse("account_create"), dict(
            username = "new_user",
            password = "test",
            password2="test"
        ), follow=True)

        resp = self.client.post(reverse('login'), {
            "username": "new_user",
            "password": "test"
        }, follow=True)

        self.assertEquals(200, resp.status_code)
        self.assertIn("Hello new_user", resp.content )

        # test for wrong input

        resp = self.client.post(reverse('login'), {
            "username": "new_user",
            "password": "wrong"
        }, follow=True)
        
        self.assertEquals(200, resp.status_code)
        self.assertIn("Please enter a correct username and password", resp.content)

        resp = self.client.post(reverse('login'), {
            "username": "wrong_user",
            "password": "test"
        }, follow=True)

        self.assertEquals(200, resp.status_code)
        self.assertIn("Please enter a correct username and password", resp.content)


class TestImageViews(TestCase):

    image_names = ("test_image",)


    def setUp(self):

        self.client.post(reverse("account_create"), dict(
            username = "new_user",
            password = "test",
            password2="test"
        ), follow=True)

        resp = self.client.post(reverse('login'), {
            "username": "new_user",
            "password": "test"
        }, follow=True)


    def tearDown(self):
        try:
            for img in self.image_names:
                path = "{0}/media/images/{1}.jpg".format(settings.ROOT_DIR, img)
                os.remove(path)
        except:
            pass

    def add_image(self):

       resp = None
       with open("core/test_files/test_image.jpg", "rb") as f:
           resp = self.client.post(reverse("image_upload"), dict(
               title = "test_image",
               img = f
           ), follow=True)

       return resp

    def test_images_are_uploaded(self):
       
       resp = self.add_image()
       self.assertEquals(200, resp.status_code )

       q = Image.objects.get()

       self.assertEquals("test_image", q.title)
       self.assertEquals("/media/images/test_image.jpg", q.img.url)
    
    def test_image_details_page(self):
        
       self.add_image()

       resp = self.client.get(reverse("image_detail", kwargs={"pk": 1}))
       self.assertEquals("test_image",resp.context["image"].title )
       self.assertIn("test_image", resp.content)
       self.assertEquals("/media/images/test_image.jpg", resp.context["image"].img.url)
       self.assertEquals("",resp.context["image"].description)

    def test_adding_image_description(self):
        self.add_image()

        resp = self.client.post(reverse("image_detail", kwargs={"pk": 1}),dict(
             description = "test description"
        ), follow=True)

        self.assertIn("test description", resp.content )
        q = Image.objects.get()
        self.assertEquals("test description",q.description)

