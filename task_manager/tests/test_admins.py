import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from task_manager.models import Position, TaskType, Task


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Debug")
        self.deadline = datetime.datetime.now().date()
        self.task = Task.objects.create(
            name="Debug new feature",
            description="Need to debug new feature in app",
            deadline=self.deadline,
            is_completed=False,
            priority="L",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker)

    def test_worker_position_name_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, "Developer")

    def test_worker_detailed_position_name_listed(self):
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        response = self.client.get(url)

        self.assertContains(response, "Developer")

    def test_worker_add_position_listed(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "Position:")

    def test_task_name_deadline_priority_listed(self):
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        deadline_str = self.deadline.strftime("%B %-d, %Y")
        fields = ("Debug new feature", deadline_str, "Low Priority")

        for field in fields:
            self.assertContains(response, field)
