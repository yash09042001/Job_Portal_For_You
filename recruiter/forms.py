from django import forms
from .models import User
from company.models import Company


class RecruiterProfileForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                     to_field_name='name')
    job_title = forms.CharField(max_length=255, required=True)
    contact_email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'avatar',
                  'dob', 'mobile']
