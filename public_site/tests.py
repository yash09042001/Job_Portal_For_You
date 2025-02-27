from django.test import TestCase
from django.urls import reverse
from job.models import Job
from company.models import Company
from recruiter.models import Recruiter
from django.contrib.auth import get_user_model

User = get_user_model()


class JobListViewTest(TestCase):
    def setUp(self):
        # Create a company
        self.company = Company.objects.create(
            name="Tech Corp",
            description="A leading tech company.",
            location="New York",
            website="https://techcorp.example.com",
            logo=None,
            benefits="Health insurance, Paid time off"
        )

        # Create a recruiter user
        self.recruiter_user = User.objects.create_user(
            email="recruiter@example.com",
            password="recruiterpass123",
            is_recruiter=True
        )
        self.recruiter = Recruiter.objects.create(
            user=self.recruiter_user,
            company=self.company,
            job_title="Senior Recruiter",
            contact_email="recruiter@example.com",
            contact_number="1234567890"
        )

        # Create jobs
        self.job1 = Job.objects.create(
            title="Software Engineer",
            recruiter=self.recruiter,
            image=None,
            description="Develop and maintain web applications.",
            status="active",
            created_at="2024-11-01",
        )
        self.job2 = Job.objects.create(
            title="Data Scientist",
            recruiter=self.recruiter,
            image=None,
            description="Analyze and interpret complex data.",
            status="active",
            created_at="2024-11-05",
        )
        self.url = reverse('public_site:job_list')

    def test_job_list_view(self):
        """Test the job list view returns correct jobs and template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/job_list.html')
        jobs = list(response.context['jobs'])
        self.assertEqual(jobs, [self.job2, self.job1])
        self.assertContains(response, self.job1.title)
        self.assertContains(response, self.job2.title)


class JobDetailViewTest(TestCase):
    def setUp(self):
        # Create a company
        self.company = Company.objects.create(
            name="Tech Corp",
            description="A leading tech company.",
            location="New York",
            website="https://techcorp.example.com",
            logo=None,
            benefits="Health insurance, Paid time off"
        )

        # Create a recruiter user
        self.recruiter_user = User.objects.create_user(
            email="recruiter@example.com",
            password="recruiterpass123",
            is_recruiter=True
        )
        self.recruiter = Recruiter.objects.create(
            user=self.recruiter_user,
            company=self.company,
            job_title="Senior Recruiter",
            contact_email="recruiter@example.com",
            contact_number="1234567890"
        )

        # Create a job
        self.job = Job.objects.create(
            title="Software Engineer",
            recruiter=self.recruiter,
            image=None,
            description="Develop and maintain web applications.",
            status="active",
            created_at="2024-11-01",
        )
        self.url = reverse(
            'public_site:job_detail', kwargs={'pk': self.job.pk})

    def test_job_detail_view(self):
        """Test the job detail view returns correct job and template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/job_detail.html')
        self.assertEqual(response.context['job'], self.job)
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.job.description)
        self.assertContains(response, self.job.qualifications)


class HomeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('public_site:home')

    def test_home_view(self):
        """Test the home view returns the correct template and status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/home.html')
        self.assertContains(response, "ok")
