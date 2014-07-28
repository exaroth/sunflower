from django.test import TestCase
from main.models import UserExt, Image
from django.contrib.auth.models import User


# Create your tests here.


class TestIndexFunctionality(TestCase):


    def test_index_is_rendering_properly(self):

        resp = self.client.get("/")
        self.assertIn("Index page", str(resp))
        self.assertEquals(resp.status_code, 200)


class TestDatabase(TestCase):


    def test_user_profiles(self):
        u = User.objects.create(username="test_user", password="test", email="test@test.com")
        p = UserExt.objects.create(user=u, portrait="/profile_images/portrait.jpg")

        sel = UserExt.objects.get(pk=1)
        self.assertEquals(sel.user.username, "test_user")
        self.assertEquals(sel.portrait, "/profile_images/portrait.jpg")


    def test_images(self):
        u = User.objects.create(username="test_user", password="test", email="test@test.com")

        i = Image.objects.create(
            title = "test_image",
            description = "test description",
            uploader = u,
            path = "/images/sample.jpg",
            thumb_path = "/thumbs/thumb_sample.jpg"
        )
        images = Image.objects.all()
        self.assertEquals(images.count(), 1)
        i = images[0]
        self.assertTrue(i.uploader.username=="test_user")
        self.assertTrue(i.title=="test_image")
        self.assertTrue(i.path=="/images/sample.jpg")

        # test for wrong input
