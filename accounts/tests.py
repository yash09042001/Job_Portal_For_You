from django.test import TestCase
from django.urls import reverse
from company.models import Company
from django.contrib.auth import get_user_model
from candidate.models import Candidate
from .models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import RecruiterRegistrationForm
from accounts.forms import CandidateRegistrationForm


class RecruiterRegistrationViewTests(TestCase):
    def setUp(self):
        # Create a sample company for the recruiter
        company = Company.objects.create(name='Amazon')
        # Mock data for recruiter registration
        self.recruiter_data = {
            'email': 'recruiter1@example.com',
            'password': 'Recruiter@123!',
            'password_confirm': 'Recruiter@123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'male',
            'mobile': '7796865755',
            'company': company,
            'job_title': 'Software Engineer',
            'contact_email': 'recruiter1@Amazon.com',
            'contact_number': '1234567890',
            }
        self.url = reverse('accounts:recruiter_register')

    def test_recruiter_registration_view_renders_correct_template(self):
        """Test if the view uses the correct template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/recruiter_register.html')

    def test_recruiter_registration_form_in_context(self):
        """Test if the form is in the context data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context['form'], RecruiterRegistrationForm)

    def test_successful_recruiter_registration(self):
        """Test successful recruiter registration."""
        response = self.client.post(self.url, self.recruiter_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        user = get_user_model().objects.get(email='recruiter1@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('Recruiter@123!'))

    def test_successful_recruiter_login(self):
        """Test successful recruiter login."""
        response = self.client.post(self.url, self.recruiter_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        get_user_model().objects.get(email='recruiter1@example.com')
        login_response = self.client.post(reverse('accounts:login'), {
            'email': 'recruiter1@example.com',
            'password': 'Recruiter@123!'
        })
        self.assertEqual(login_response.status_code, 200)


class CandidateRegistrationViewTest(TestCase):
    def setUp(self):
        # Example recruiter data
        self.candidate_data = {
            'email': 'candidate1@example.com',
            'password': 'strongpassword1234',
            'password_confirm': 'strongpassword1234',
            'first_name': 'Joy',
            'last_name': 'Roy',
            'gender': 'male',
            'mobile': '7796065755',
            'skill': 'css,html',
            'experience': '11',
            }
        self.url = reverse('accounts:candidate_register')

    def test_candidate_registration_view_renders_correct_template(self):
        """Test if the view uses the correct template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/candidate_register.html')

    def test_candidate_registration_form_in_context(self):
        """Test if the form is in the context data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context['form'], CandidateRegistrationForm)

    def test_successful_candidate_registration(self):
        """Test that a candidate can register successfully with valid data."""
        # Prepare form data
        form_data = {
            'first_name': 'Joy',
            'last_name': 'Roy',
            'gender': 'male',
            'email': 'candidate1@example.com',
            'mobile': '7796065755',
            'password': 'strongpassword1234',
            'password_confirm': 'strongpassword1234',
            'skill': 'css,html',
            'experience': '11.0',
            'cv': SimpleUploadedFile(
                "cv.pdf", b"dummy data", content_type="application/pdf"),
            'portfolio': 'https://portfolio.example.com',
        }

        # Simulate a POST request
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('accounts:login'))
        user = User.objects.get(email='candidate1@example.com')
        self.assertEqual(user.first_name, 'Joy')
        self.assertEqual(user.last_name, 'Roy')
        self.assertTrue(user.is_candidate)
        self.assertTrue(user.check_password('strongpassword1234'))
        candidate = Candidate.objects.get(user=user)
        self.assertEqual(candidate.skill, 'css,html')
        self.assertEqual(candidate.experience, 11.0)
        self.assertEqual(candidate.portfolio, 'https://portfolio.example.com')
        self.assertIsNotNone(candidate.cv)

    def test_successful_candidate_login(self):
        """Test successful candidate login."""
        self.client.post(self.url, self.candidate_data)
        login_response = self.client.post(reverse('accounts:login'), {
            'email': 'candidate1@example.com',
            'password': 'Candidate@123!',
        })
        self.assertEqual(login_response.status_code, 200)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='candidate@gmali.com', password='testpassword')

    def test_login_access(self):
        """Test login access"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
