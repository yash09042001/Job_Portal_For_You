from django import forms
from .models import User


class CandidateProfileForm(forms.ModelForm):
    skill = forms.CharField(max_length=255, required=True)
    experience = forms.FloatField(help_text='In Months', required=True)
    cv = forms.FileField(required=True)
    portfolio = forms.URLField(help_text='Link URL', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email',
                  'mobile']
