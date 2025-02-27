from django.db import models
from accounts.models import User


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill = models.TextField()
    experience = models.FloatField(help_text='In Months')
    cv = models.FileField(upload_to='cv/')
    portfolio = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
