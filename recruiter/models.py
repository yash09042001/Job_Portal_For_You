from django.db import models
from company.models import Company
from accounts.models import User


class Recruiter(models.Model):
    """Recruiter model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.company.name})'
