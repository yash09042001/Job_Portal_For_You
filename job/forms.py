from django import forms
from job.models import Job
from django.utils.timezone import now


class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'image', 'description', 'qualifications',
                  'deadlines', 'status']
    
    def clean_deadlines(self):
        deadlines = self.cleaned_data.get('deadlines')
        if deadlines is None:
            raise forms.ValidationError("The deadlines field is required.")
        if deadlines <= now().date():
            raise forms.ValidationError("The deadline must be a future date.")
        return deadlines