from django.db import models
from recruiter.models import Recruiter
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import timedelta


class Job(models.Model):
    title = models.CharField(max_length=100)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jobimage/', blank=True)
    description = models.TextField()
    qualifications = models.TextField(max_length=255)
    deadlines = models.DateField(default=now().date() + timedelta(days=7))
    status = models.CharField(
        max_length=50,
        choices=[
            ('open', 'Open'),
            ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.deadlines is None:
            raise ValidationError("The deadlines field cannot be empty.")
        if self.deadlines <= now().date():
            raise ValidationError("The deadline must be a future date.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
