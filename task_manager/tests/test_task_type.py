from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType


class PublicTaskTypeTests(TestCase):
    def test_task_type_list_login_required(self):
        url = reverse("manager:task-type-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        url = reverse("manager:task-type-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_delete_login_required(self):
        task_type = TaskType.objects.create(
            name="Debug",
        )
        url = reverse("manager:task-type-delete", args=[task_type.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_task_type_list(self):
        TaskType.objects.create(name="Debug")
        TaskType.objects.create(name="QA")

        url = reverse("manager:task-type-list")
        response = self.client.get(url)

        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types)
        )

    def test_task_type_search_by_name(self):
        TaskType.objects.create(name="Debug")
        TaskType.objects.create(name="QA")
        TaskType.objects.create(name="Create")

        url = reverse("manager:task-type-list") + "?name=a"
        response = self.client.get(url)

        task_types_contains_a = TaskType.objects.filter(
            name__icontains="a"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types_contains_a)
        )

    def test_task_type_create(self):
        data = {
            "name": "Debug",
        }
        url = reverse("manager:task-type-create")
        response = self.client.post(url, data=data)

        self.assertEqual(TaskType.objects.last().name, "Debug")
        self.assertRedirects(response, reverse("manager:task-type-list"))

    def test_task_type_delete(self):
        task_type = TaskType.objects.create(
            name="Debug",
        )
        url = reverse("manager:task-type-delete", args=[task_type.id])
        response = self.client.post(url)

        task_types = TaskType.objects.all()

        self.assertFalse(task_type in task_types)
        self.assertRedirects(response, reverse("manager:task-type-list"))
