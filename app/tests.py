from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

User = get_user_model()
# Create your tests here.
class UpdateProfileViewTest(TestCase):
    def setUp(self):
        # Create a user and a profile
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="testpassword"
        )
        self.profile = Profile.objects.create(
            user_id=self.user,
            phone_number="1234567890",
            address="123 Old Street",
            city="Old City",
            state="Old State",
            Country="Old Country"
        )

        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Update data
        self.update_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "profile": {
                "phone_number": "9876543210",
                "address": "456 New Street",
                "city": "New City",
                "state": "New State",
                "Country": "New Country"
            }
        }

    def test_update_profile(self):
        # Send a PUT request to the update endpoint
        response = self.client.put('/profile/update/', self.update_data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch the updated user and profile
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        # Assert user data
        self.assertEqual(self.user.username, "newuser")
        self.assertEqual(self.user.email, "newuser@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")

        # Assert profile data
        self.assertEqual(self.profile.phone_number, "9876543210")
        self.assertEqual(self.profile.address, "456 New Street")
        self.assertEqual(self.profile.city, "New City")
        self.assertEqual(self.profile.state, "New State")
        self.assertEqual(self.profile.Country, "New Country")


    def test_login_invalid_credentials(self):
        # Register the user first
        self.client.post('/api/register/', self.registration_data, format='json')

        # Incorrect login credentials
        invalid_login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        # Send POST request
        response = self.client.post('/api/login/', invalid_login_data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('non_field_errors', response.data)

    def test_login_invalid_credentials(self):
        # Register the user first
        self.client.post('/api/register/', self.registration_data, format='json')

        # Incorrect login credentials
        invalid_login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        # Send POST request
        response = self.client.post('/api/login/', invalid_login_data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('non_field_errors', response.data)

    def test_user_registration(self):
        # Send POST request to the registration endpoint
        response = self.client.post('/api/register/', self.registration_data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user was created
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

        # Check if the profile was created
        profile = Profile.objects.get(user_id=user)
        self.assertEqual(profile.phone_number, "1234567890")
        self.assertEqual(profile.address, "123 Main Street")
        self.assertEqual(profile.city, "Test City")
        self.assertEqual(profile.state, "Test State")
        self.assertEqual(profile.Country, "Test Country")
