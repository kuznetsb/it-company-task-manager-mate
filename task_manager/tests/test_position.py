from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position


class PublicPositionTests(TestCase):
    def test_position_list_login_required(self):
        url = reverse("manager:position-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_position_create_login_required(self):
        url = reverse("manager:position-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_position_delete_login_required(self):
        position = Position.objects.create(
            name="Developer",
        )
        url = reverse("manager:position-delete", args=[position.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_position_list(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Tester")

        url = reverse("manager:position-list")
        response = self.client.get(url)

        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )

    def test_position_search_by_name(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Tester")
        Position.objects.create(name="Office Manager")

        url = reverse("manager:position-list") + "?name=d"
        response = self.client.get(url)

        positions_contains_d = Position.objects.filter(
            name__icontains="d"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions_contains_d)
        )

    def test_position_create(self):
        data = {
            "name": "Developer",
        }
        url = reverse("manager:position-create")
        response = self.client.post(url, data=data)

        self.assertEqual(Position.objects.last().name, "Developer")
        self.assertRedirects(response, reverse("manager:position-list"))

    def test_position_delete(self):
        position = Position.objects.create(
            name="Developer",
        )
        url = reverse("manager:position-delete", args=[position.id])
        response = self.client.post(url)

        positions = Position.objects.all()

        self.assertFalse(position in positions)
        self.assertRedirects(response, reverse("manager:position-list"))
