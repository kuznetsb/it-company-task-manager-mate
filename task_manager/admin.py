from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import TaskType, Position, Worker, Task
from task_manager.custom_choices_filter import AllValuesChoicesFieldListFilter


admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Position info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Position info", {"fields": ("position",)}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "deadline",
        "is_completed",
        "get_priority",
    ]
    list_filter = [
        "is_completed",
        ("priority", AllValuesChoicesFieldListFilter),
        "assignees"
    ]
    search_fields = ["name"]

    def get_priority(self, obj):
        return obj.get_priority_display()

    get_priority.short_description = "Priority"
