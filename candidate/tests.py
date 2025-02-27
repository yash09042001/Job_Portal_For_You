from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Candidate
User = get_user_model()


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='candidate1@example.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe',
        )
        self.user.is_candidate = True
        self.user.save()

    def test_profile_view_access(self):
        """Test that a logged-in candidate can access the profile view."""
        self.client.login(
            email='candidate1@example.com', password='testpassword123')
        response = self.client.get(reverse('candidate:cprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidate/cprofile.html')


class CandidateProfileUpdateViewTest(TestCase):
    def setUp(self):
        # Create a user and associate it with a candidate profile
        self.user = User.objects.create_user(
            email='candidate1@example.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe',
        )
        self.user.is_candidate = True
        self.user.save()

        self.candidate = Candidate.objects.create(
            user=self.user, skill="Python", experience=3.5)

        # Define the URL for profile update view
        self.url = reverse('candidate:ceditprofile')

    def test_profile_update_view_access(self):
        """Test that logged-in candidate can access the profileupdate view."""
        self.client.login(
            email='candidate1@example.com', password='testpassword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidate/ceditprofile.html')
