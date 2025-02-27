from django.test import TestCase
from django.contrib.auth import get_user_model
from recruiter.models import Recruiter
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from company.models import Company
from candidate.models import Candidate
from application.models import Application
from job.models import Job

User = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        # Create a company
        self.company = Company.objects.create(
            name="Tech Corp",
            description="A leading tech company.",
            location="New York",
            website="https://techcorp.example.com",
            logo=None,  # Replace with a valid file in actual test
            benefits="Health insurance, Paid time off"
        )
        # Create a recruiter user
        self.recruiter_user = User.objects.create_user(
            email="recruiter@example.com",
            password="password123",
            mobile='9876543220',
            is_recruiter=True
        )
        # Create a recruiter profile linked to the company
        self.recruiter = Recruiter.objects.create(
            user=self.recruiter_user,
            company=self.company,
            job_title="HR Manager",
            contact_email="hr@techcorp.example.com",
            contact_number="1234567890"
        )
        # Create a candidate user
        self.candidate_user = User.objects.create_user(
            email='candidate1@example.com',
            password='testpassword123',
            mobile='9876543210',
            is_candidate=True
        )
        # Create a candidate profile for the created candidate_user
        self.candidate = Candidate.objects.create(
            user=self.candidate_user,  # Link the candidate profile to the user
            skill="Python, Django",
            experience="2",
            cv=SimpleUploadedFile(
                "cv.pdf", b"dummy data", content_type="application/pdf"),
            portfolio="https://candidateportfolio.example.com"
        )
        # Create applications for the candidate
        job1 = Job.objects.create(
            title="Software Developer",
            recruiter=self.recruiter,
            description="Develop software",
            status="active",
            created_at="2024-11-01"
        )

        job2 = Job.objects.create(
            title="Data Scientist",
            recruiter=self.recruiter,
            description="Analyze data",
            status="active",
            created_at="2024-11-01"
        )

        # Create applications for the candidate
        Application.objects.create(
            job=job1,
            candidate=self.candidate,
            cover_letter="I am very interested in this job.",
            status="in process",
            created_at="2024-11-10"
        )
        Application.objects.create(
            job=job2,
            candidate=self.candidate,
            cover_letter="I am very interested in this job.",
            status="in process",
            created_at="2024-11-11"
        )
        self.url = '/dashboard/'

    def test_dashboard_recruiter_view(self):
        """Test dashboard context data for a recruiter."""
        self.client.login(
            email="recruiter@example.com", password="password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashborad.html')

        # Check context data for recruiter
        self.assertEqual(response.context['job_count'], 2)
        self.assertEqual(response.context['total_received_applications'], 2)
        self.assertTrue(response.context['is_recruiter'])
        self.assertNotIn('is_candidate', response.context)

    def test_dashboard_candidate_view(self):
        """Test dashboard context data for a candidate."""
        self.client.login(
            email='candidate1@example.com', password='testpassword123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashborad.html')

        # Check context data for candidate
        self.assertEqual(response.context['application_count'], 2)
        self.assertEqual(response.context['in_process_count'], 0)
        self.assertEqual(response.context['interview_scheduled_count'], 0)
        self.assertEqual(response.context['accepted_count'], 0)
        self.assertEqual(response.context['rejected_count'], 0)
        self.assertTrue(response.context['is_candidate'])
        self.assertNotIn('is_recruiter', response.context)

    def test_dashboard_unauthenticated_user(self):
        """Test redirection for unauthenticated users."""
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f"{reverse(
                'accounts:login')}?next={reverse('dashboard:dashboard')}")
