from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Название проекта'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5, 'placeholder': 'Описание'})
        self.fields['github_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'https://github.com/...'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})