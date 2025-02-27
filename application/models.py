from django.db import models
from job.models import Job
from candidate.models import Candidate


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted')
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='applied')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.candidate} applied for {self.job}'
