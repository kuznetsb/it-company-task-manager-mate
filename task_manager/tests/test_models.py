import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase


from task_manager.models import Task, TaskType, Position


class ModelsTest(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Debug")

        self.assertEqual(str(task_type), "Debug")

    def test_position_str(self):
        position = TaskType.objects.create(name="Developer")

        self.assertEqual(str(position), "Developer")

    def test_create_worker_with_position(self):
        position = Position.objects.create(name="Developer")
        worker = get_user_model().objects.create_user(
            username="test_user",
            password="user12345",
            position=position
        )

        self.assertEqual(worker.username, "test_user")
        self.assertTrue(worker.check_password("user12345"))
        self.assertEqual(worker.position, position)

    def test_task_completed_str(self):
        date = datetime.datetime.now().date()
        task_type = TaskType.objects.create(name="Debug")
        task = Task.objects.create(
            name="Create new app",
            deadline=date,
            is_completed=True,
            task_type=task_type
        )

        self.assertEqual(
            str(task),
            f"Create new app (Deadline: {date}, Status: Completed)"
        )

    def test_task_uncompleted_str(self):
        date = datetime.datetime.now().date()
        task_type = TaskType.objects.create(name="Debug")
        task = Task.objects.create(
            name="Create new app",
            deadline=date,
            is_completed=False,
            task_type=task_type
        )

        self.assertEqual(
            str(task),
            f"Create new app (Deadline: {date}, Status: Not Completed)"
        )
