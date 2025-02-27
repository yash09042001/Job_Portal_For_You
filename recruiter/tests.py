from django.test import TestCase
from accounts.models import User
from django.urls import reverse
from .models import Recruiter
from company.models import Company


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='recruiter1@example.com',
            password='Recruiter@123!',
            first_name='John',
            last_name='Doe',
        )
        self.user.is_recruiter = True
        self.user.save()

    def test_profile_view_access(self):
        """Test that a logged-in recruiter can access the profile view."""
        self.client.login(
            email='recruiter1@example.com', password='Recruiter@123!')
        response = self.client.get(reverse('recruiter:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter/profile.html')


class RecruiterProfileUpdateViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='recruiter1@example.com',
            password='Recruiter@123!',
            first_name='John',
            last_name='Doe',
        )
        self.user.is_recruiter = True
        self.user.save()

        # Create a company
        self.company = Company.objects.create(
            name="Tech Corp",
            description="A leading tech company",
            location="New York",
            website="https://techcorp.com",
        )

        # Create a recruiter associated with the user and the company
        self.recruiter = Recruiter.objects.create(
            user=self.user,
            company=self.company,
            job_title="HR Manager",
            contact_email="hr@techcorp.com",
            contact_number="1234567890",
        )

        # Define the URL for the profile update view
        self.url = reverse('recruiter:reditprofile')

    def test_profile_update_view_access(self):
        """Test that logged-in recruiter can access the profileupdate view."""
        self.client.login(
            email='recruiter1@example.com', password='Recruiter@123!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruiter/reditprofile.html')
