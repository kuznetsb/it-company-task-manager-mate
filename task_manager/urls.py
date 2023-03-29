from django.urls import path

from task_manager.views import (
    index,
    TaskListView,
    PositionCreateView,
    TaskTypeCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "position/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "task_type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
]

app_name = "manager"
