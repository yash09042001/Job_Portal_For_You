from django.contrib import admin
from .models import Job
from recruiter.models import Recruiter

# Register your models here.


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'created_at', 'status')
    list_filter = ('status', 'recruiter')
    search_fields = ('title', 'recruiter__company__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recruiter":
            kwargs["queryset"] = Recruiter.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Job, JobAdmin)
