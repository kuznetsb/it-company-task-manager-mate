import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType


class PublicTaskTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="Debug"
        )
        self.deadline = datetime.datetime.now().date()
        self.task = Task.objects.create(
            name="Fix bug",
            deadline=self.deadline,
            is_completed=False,
            task_type=self.task_type
        )

    def test_task_list_login_required(self):
        url = reverse("manager:task-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_create_login_required(self):
        url = reverse("manager:task-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_update_login_required(self):
        url = reverse("manager:task-update", args=[self.task.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_login_required(self):
        url = reverse("manager:task-delete", args=[self.task.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(
            name="Debug"
        )
        self.deadline = datetime.datetime.now().date()
        self.task = Task.objects.create(
            name="Fix bug",
            deadline=self.deadline,
            is_completed=False,
            task_type=self.task_type
        )

    def test_retrieve_task_list(self):
        dev_task = TaskType.objects.create(name="Develop")
        Task.objects.create(
            name="Create app",
            deadline=self.deadline,
            is_completed=True,
            task_type=dev_task
        )

        url = reverse("manager:task-list")
        response = self.client.get(url)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )

    def test_task_search_by_name(self):
        dev_task = TaskType.objects.create(name="Develop")
        Task.objects.create(
            name="Create app",
            deadline=self.deadline,
            is_completed=True,
            task_type=dev_task
        )

        url = reverse("manager:task-list") + "?name=d"
        response = self.client.get(url)

        tasks_contains_d = Task.objects.filter(
            name__icontains="d"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks_contains_d)
        )

    def test_task_create(self):
        dev_task = TaskType.objects.create(name="Develop")
        data = {
            "name": "Create app",
            "description": "",
            "deadline": str(self.deadline),
            "is_completed": "on",
            "priority": "H",
            "task_type": dev_task.id,
            "assignees": self.user.id
        }
        url = reverse("manager:task-create")
        response = self.client.post(url, data=data)
        created_task = Task.objects.get(name="Create app")

        self.assertEqual(created_task.deadline, self.deadline)
        self.assertEqual(created_task.task_type, dev_task)
        self.assertEqual(created_task.assignees.all()[0], self.user)
        self.assertRedirects(response, reverse("manager:task-list"))

    def test_task_update(self):
        data = {
            "name": "Create app",
            "description": "",
            "deadline": str(self.deadline),
            "is_completed": "on",
            "priority": "L",
            "task_type": self.task.task_type.id,
            "assignees": self.user.id
        }
        url = reverse("manager:task-update", args=[self.task.id])
        response = self.client.post(url, data=data)
        updated_task = Task.objects.get(id=self.task.id)

        self.assertEqual(updated_task.name, "Create app")
        self.assertEqual(updated_task.is_completed, True)
        self.assertEqual(updated_task.get_priority_display(), "Low Priority")
        self.assertEqual(updated_task.assignees.all()[0], self.user)
        self.assertRedirects(response, reverse("manager:task-detail", args=[self.task.id]))

    def test_task_delete(self):
        url = reverse("manager:task-delete", args=[self.task.id])
        response = self.client.post(url)

        tasks = Task.objects.all()

        self.assertFalse(self.task in tasks)
        self.assertRedirects(response, reverse("manager:task-list"))
