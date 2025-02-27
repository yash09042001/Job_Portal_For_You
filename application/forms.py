from django import forms
from .models import Application


class ApplicationCreationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'row': 4, 'placeholder': 'Write you cover letter here.....'})
        }
