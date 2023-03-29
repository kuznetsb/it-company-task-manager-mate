import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from task_manager.models import Task


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
