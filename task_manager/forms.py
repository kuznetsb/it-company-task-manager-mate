from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Worker, Position


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "select a date",
                "type": "date"
            }
        ),
    )

    class Meta:
        model = Task
        fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        required=False,
        queryset=Position.objects.all()
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        required=False,
        queryset=Position.objects.all()
    )

    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "position"]


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by task type name..."}
        )
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by position name..."}
        )
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by task name..."}
        )
    )


class WorkerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by worker first name..."}
        )
    )
