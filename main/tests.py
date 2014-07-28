from django.test import TestCase

# Create your tests here.


class TestIndexFunctionality(TestCase):


    def test_index_is_rendering_properly(self):

        resp = self.client.get("/")
        self.assertIn("Index page", str(resp))
        self.assertEquals(resp.status_code, 200)
