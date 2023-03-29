from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task


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
