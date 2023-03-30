from django.test import TestCase

from task_manager.forms import WorkerCreationForm
from task_manager.models import Position


class FormTests(TestCase):
    def test_worker_creation_form_with_custom_fields(self):
        position = Position.objects.create(name="Developer")
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "position": position,
            "first_name": "Test",
            "last_name": "User",
        }

        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_creation_form_with_custom_fields_invalid(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "position": "developer",
            "first_name": "Test",
            "last_name": "User",
        }

        form = WorkerCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
