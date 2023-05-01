from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicIndexTests(TestCase):
    def test_index_login_required(self):
        url = reverse("manager:index")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_index_zero_tasks(self):
        url = reverse("manager:index")
        response = self.client.get(url)

        self.assertEqual(response.context["percentage"], 100)
