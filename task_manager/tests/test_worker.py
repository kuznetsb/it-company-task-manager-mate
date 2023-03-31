import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, TaskType, Task


class PublicWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="CEO")

    def test_worker_list_login_required(self):
        url = reverse("manager:worker-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_login_required(self):
        url = reverse("manager:worker-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_login_required(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            position=self.position
        )
        url = reverse("manager:worker-update", args=[user.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_delete_delete_login_required(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            position=self.position
        )
        url = reverse("manager:worker-delete", args=[user.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="admin_user",
            password="test98765"
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="CEO")

    def test_retrieve_worker_list(self):
        get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            position=self.position
        )

        url = reverse("manager:worker-list")
        response = self.client.get(url)

        users = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(users)
        )

    def test_retrieve_worker_detail_page(self):
        task_type = TaskType.objects.create(
            name="Fix",
        )
        date = datetime.datetime.now().date()
        task = Task.objects.create(
            name="Fix something",
            deadline=date,
            is_completed=False,
            task_type=task_type
        )
        task.assignees.add(self.user)

        url = reverse("manager:worker-detail", args=[self.user.id])
        response = self.client.get(url)

        tasks = self.user.tasks.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker"].tasks.all()),
            list(tasks)
        )

    def test_worker_search_by_first_name(self):
        get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            first_name="Jack",
            position=self.position
        )
        get_user_model().objects.create_user(
            username="test_2",
            password="test54321",
            first_name="John",
            position=self.position
        )

        url = reverse("manager:worker-list") + "?first_name=j"
        response = self.client.get(url)

        first_name_contains_j = get_user_model().objects.filter(
            first_name__icontains="j"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(first_name_contains_j)
        )

    def test_worker_create(self):
        data = {
            "username": "test_1",
            "password1": "test12345",
            "password2": "test12345",
            "position": self.position.id,
            "first_name": "",
            "last_name": "",
            "email": ""
        }
        url = reverse("manager:worker-create")
        response = self.client.post(url, data=data)

        new_user = get_user_model().objects.get(username="test_1")
        self.assertTrue(new_user.check_password("test12345"))
        self.assertEqual(new_user.position, self.position)
        self.assertRedirects(
            response,
            reverse("manager:worker-list")
        )

    def test_worker_update(self):
        data = {
            "position": self.position.id,
            "first_name": "",
            "last_name": "",
            "email": ""
        }
        url = reverse("manager:worker-update", args=[self.user.id])
        response = self.client.post(url, data=data)

        self.assertEqual(
            get_user_model().objects.get(
                id=self.user.id).position, self.position
        )
        self.assertRedirects(
            response,
            reverse("manager:worker-detail", args=[self.user.id])
        )

    def test_worker_delete(self):
        user = get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            first_name="Jack",
            position=self.position
        )
        url = reverse("manager:worker-delete", args=[user.id])
        response = self.client.post(url)

        users = get_user_model().objects.all()

        self.assertFalse(user in users)
        self.assertRedirects(response, reverse("manager:worker-list"))

    def test_assign_to_task(self):
        task_type = TaskType.objects.create(
            name="Fix",
        )
        date = datetime.datetime.now().date()
        task = Task.objects.create(
            name="Fix something",
            deadline=date,
            is_completed=False,
            task_type=task_type
        )

        url = reverse("manager:task-assign-worker", args=[task.id])
        response = self.client.get(url)

        self.assertEqual(
            list(task.assignees.all()),
            [response.wsgi_request.user]
        )
        self.assertRedirects(
            response, reverse("manager:task-detail", args=[task.id])
        )

    def test_discharge_from_task(self):
        task_type = TaskType.objects.create(
            name="Fix",
        )
        date = datetime.datetime.now().date()
        task = Task.objects.create(
            name="Fix something",
            deadline=date,
            is_completed=False,
            task_type=task_type
        )
        task.assignees.add(self.user)

        url = reverse("manager:task-assign-worker", args=[task.id])
        response = self.client.get(url)

        self.assertEqual(list(task.assignees.all()), [])
        self.assertRedirects(
            response, reverse("manager:task-detail", args=[task.id])
        )
