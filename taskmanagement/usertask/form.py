from django import forms
from .models import Task


class insert_form(forms.ModelForm):
    class Meta:
        model = Task
        fields =  ['status', 'completion_report', 'worked_hours']