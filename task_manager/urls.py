from django.urls import path

from task_manager.views import (
    index,
    TaskListView,
    PositionCreateView,
    TaskTypeCreateView,
    TaskDetailView
)

urlpatterns = [
    path("", index, name="index"),
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
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail")
]

app_name = "manager"
