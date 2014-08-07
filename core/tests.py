from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

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

    def test_showing_no_images_when_no_images(self):

        resp = self.client.get(reverse("index"))
        self.assertIn("No pictures uploaded yet", resp.content)

    def test_adding_images(self):

        self.create_sample_image()
        resp = self.client.get(reverse("index"))
        image = resp.context["images"][0]
        self.assertEquals("test image", image.title)
        self.assertNotIn("No pictures uploaded yet", resp.content)


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
            homepage="http://www.test.com/",
            portrait="portrait.jpg"
        ), follow=True)

        user_data = User.objects.filter(username__exact="new_user2").get()
        additional_data = UserProfile.objects.get(user=user_data)
        self.assertEquals(additional_data.homepage, u"http://www.test.com/")

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

