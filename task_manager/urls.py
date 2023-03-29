from django.urls import path

from task_manager.views import (
    index,
    PositionCreateView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
    TaskListView,
    TaskDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "position/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task_type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task_type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail")
]

app_name = "manager"
