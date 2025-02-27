from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recruiter.models import Recruiter
from company.models import Company
from candidate.models import Candidate
from .models import Job

User = get_user_model()


class JobCreateViewTest(TestCase):
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
            email="candidate@example.com",
            password="password123",
            mobile='9876543210',
            first_name='Joy',
            last_name='Roy',
            gender='male',
            is_candidate=True
        )
        # Create a job listing
        self.job = Job.objects.create(
            title="Software Developer",
            description="Develop software applications",
            qualifications="B.Sc. in Computer Science",
            status="open",
            recruiter=self.recruiter
        )
        self.url = reverse(
            'application:apply_job', kwargs={'job_id': self.job.id})
        # URL for the job create view
        self.url = reverse('job:create_job')

    def test_job_create_view_access(self):
        """Test that a logged-in recruiter can access the view"""
        self.client.login(
            email="recruiter@example.com", password="password123",)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/create_job.html')

    def test_create_job_application(self):
        """Test that the logged recruiter create job"""
        self.client.login(
            email="recruiter@example.com", password="password123",)
        # Define job creation data
        data = {
            'title': 'Software Developer',
            'description': 'Develop software applications',
            'qualifications': 'B.Sc. in Computer Science',
            'deadlines': '2024-12-01',
            'status': 'open',
        }
        response = self.client.post(self.url, data)
        job = Job.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:dashboard'))
        self.assertEqual(job.title, 'Software Developer')
        self.assertEqual(job.description, 'Develop software applications')
        self.assertEqual(job.qualifications, 'B.Sc. in Computer Science')
        self.assertEqual(job.deadlines.strftime('%Y-%m-%d'), '2024-12-01')
        self.assertEqual(job.status, 'open')
        self.assertEqual(job.recruiter, self.recruiter)
        self.assertTrue(job.created_at)


class ActiveJobListViewTest(TestCase):
    def setUp(self):
        # Create a candidate user
        self.candidate_user = User.objects.create_user(
            email="candidate@example.com",
            password="password123",
            is_candidate=True
        )
        self.candidate = Candidate.objects.create(
            user=self.candidate_user,
            skill="Python, Django",
            experience="2.0",
            cv=None,  # Add a valid file path if needed for testing
            portfolio="https://candidate-portfolio.example.com"
        )
        # Create a company
        self.company = Company.objects.create(
            name="Tech Corp",
            description="A leading tech company.",
            location="New York",
            website="https://techcorp.example.com",
            logo=None,  # Add a valid file path if testing requires it
            benefits="Health insurance, Paid time off"
        )
        self.url = reverse('job:active_job_list')

    def test_active_job_list_view_access_for_candidate(self):
        """Test that logged-in candidate can access the active job list view"""
        self.client.login(
            email="candidate@example.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/active_job_list.html')


class ActiveJobDetailViewTest(TestCase):
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
            company=self.company,  # Pass the company instance here
            job_title="Senior Recruiter",
            contact_email="recruiter@example.com",
            contact_number="1234567890"
        )

        # Create a candidate user
        self.candidate_user = User.objects.create_user(
            email="candidate@example.com",
            password="password123",
            mobile="9876543210",
            is_candidate=True
        )
        self.candidate = Candidate.objects.create(
            user=self.candidate_user,
            skill="Python, Django",
            experience="2.0",
            cv=None,
            portfolio="https://candidate-portfolio.example.com"
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
        self.url = reverse('job:active_job_detail', kwargs={'pk': self.job.pk})

    def test_active_job_detail_view_access_for_candidate(self):
        """Test logged-in candidate can access the active job detail view"""
        self.client.login(
            email="candidate@example.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/active_job_detail.html')
        self.assertEqual(response.context['job'], self.job)
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.job.description)

    def test_active_job_detail_view_access_for_recruiter(self):
        """Test logged-in recruiter can access the active job detail view"""
        self.client.login(
            email="recruiter@example.com", password="recruiterpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/active_job_detail.html')
        self.assertEqual(response.context['job'], self.job)
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.job.description)
