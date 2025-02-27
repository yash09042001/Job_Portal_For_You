from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from candidate.models import Candidate
from recruiter.models import Recruiter
from company.models import Company
from job.models import Job
from application.models import Application
User = get_user_model()


class ApplicationCreateViewTest(TestCase):
    def setUp(self):
        # Create a company
        self.company = Company.objects.create(
            name="Tech Solutions",
            description="A leading tech company.",
            location="New York",
            website="https://www.techsolutions.com",
            benefits="Health insurance, flexible hours"
        )

        # Create a candidate user
        self.user = User.objects.create_user(
            email='candidate1@example.com',
            password='strongpassword1234',
            first_name='Joy',
            last_name='Roy',
            gender='male',
            mobile='7796065755'
            )
        self.candidate = Candidate.objects.create(
            user=self.user, skill="Python", experience=3.5)
        # Create a recruiter user
        self.recruiter_user = User.objects.create_user(
            email='recruiter1@example.com',
            password='Recruiter@123!',
            first_name='John',
            last_name='Doe',
            gender='male',
            mobile='7796865755',
            )
        self.recruiter = Recruiter.objects.create(
            user=self.recruiter_user,
            company=self.company,
            job_title="HR Manager",
            contact_email="hr@company.com",
            contact_number="1234567890"
        )

        # Create a job
        self.job = Job.objects.create(
            title="Test Job",
            recruiter=self.recruiter,
            description="Test Description",
            status="open"
        )

        self.url = reverse(
            'application:apply_job', kwargs={'job_id': self.job.id})

    def test_application_create_view_access(self):
        """Test that a logged-in candidate can access the view"""
        self.client.login(
            email='candidate1@example.com', password="strongpassword1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/apply.html')

    def test_submit_job_application(self):
        """Test that logged candidate submit job application"""
        self.client.login(
            email='candidate1@example.com', password="strongpassword1234")
        application_data = {
            'cover_letter': 'I am very interested in this job.',
        }
        response = self.client.post(self.url, data=application_data)
        self.assertEqual(response.status_code, 302)
        application = Application.objects.filter(
            job=self.job, candidate=self.candidate).first()
        self.assertIsNotNone(application)
        self.assertEqual(
            application.cover_letter, 'I am very interested in this job.')

    def test_successful_application_redirect(self):
        """Test that logged candidate after submit job rediect"""
        self.client.login(
            email='candidate1@example.com', password="strongpassword1234")
        application_data = {
            'cover_letter': 'Excited to apply for this role!',
        }
        response = self.client.post(self.url, data=application_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse(
                'job:active_job_detail', kwargs={'pk': self.job.id}))
