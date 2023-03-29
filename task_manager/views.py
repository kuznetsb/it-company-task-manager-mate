import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskForm, WorkerCreationForm, WorkerPositionUpdateForm
from task_manager.models import Task, TaskType, Position, Worker


@login_required
def index(request):
    """View function for the home page of the site."""
    today = datetime.datetime.now().date()

    num_all_tasks = Task.objects.count()
    num_tasks_done = Task.objects.filter(is_completed=True).count()
    num_workers = get_user_model().objects.count()
    today_tasks = Task.objects.filter(deadline=today)

    context = {
        "num_all_tasks": num_all_tasks,
        "num_tasks_done": num_tasks_done,
        "num_workers": num_workers,
        "today_tasks": today_tasks,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    context_object_name = "task_type"
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    queryset = Task.objects.select_related(
        "task_type").prefetch_related("assignees")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type").prefetch_related("assignees__position")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("manager:task-detail", kwargs={"pk": pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = get_user_model().objects.select_related("position")
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = get_user_model().objects.prefetch_related("tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("manager:worker-detail", kwargs={"pk": pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
