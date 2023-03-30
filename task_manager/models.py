from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"


class Task(models.Model):
    TASK_IMPORTANCE_CHOICES = {
        ("U", "Urgent"),
        ("H", "High Priority"),
        ("L", "Low Priority")
    }

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=1,
        choices=TASK_IMPORTANCE_CHOICES,
        default="H"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )

    class Meta:
        ordering = ["deadline"]

    def __str__(self) -> str:
        status = "Completed" if self.is_completed else "Not Completed"
        return f"{self.name} (Deadline: {self.deadline}, Status: {status})"
