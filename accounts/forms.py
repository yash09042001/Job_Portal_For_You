from django import forms
from .models import User
from django.contrib.auth import get_user_model
from company.models import Company
from recruiter.models import Recruiter
from candidate.models import Candidate

user = get_user_model()


class RecruiterRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                     to_field_name='name')
    job_title = forms.CharField(max_length=255, required=True)
    contact_email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'avatar',
                  'dob', 'mobile', 'password',]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            Recruiter.objects.create(
                user=user,
                company=self.cleaned_data['company'],
                job_title=self.cleaned_data['job_title'],
                contact_email=self.cleaned_data['contact_email'],
                contact_number=self.cleaned_data['contact_number']
            )
        return user


class CandidateRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    skill = forms.CharField(max_length=255, required=True)
    experience = forms.FloatField(help_text='In Months', required=True)
    cv = forms.FileField(required=True)
    portfolio = forms.URLField(help_text='Link URL', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email',
                  'mobile', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_candidate = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Candidate.objects.create(
                user=user,
                skill=self.cleaned_data['skill'],
                experience=self.cleaned_data['experience'],
                cv=self.cleaned_data['cv'],
                portfolio=self.cleaned_data['portfolio']
            )
        return user
