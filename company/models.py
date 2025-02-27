from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
