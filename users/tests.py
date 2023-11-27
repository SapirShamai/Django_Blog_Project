"""
Module: tests.py

This module contains test cases for the users app, covering user profile creation, registration views, and form validations.

Classes:
    UserProfileTestCase: Test case for user profile creation and deletion.
    UserRegistrationTestCase: Test case for user registration views and form validations.
    UserFormsTestCase: Test case for user and profile form validations.

"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.messages import get_messages


class UserProfileTestCase(TestCase):
    def setUp(self):
        """
        Set up test data for user and profile.

        Creates a test user and profile for testing user profile creation.

        """
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'

        # Check if the test user exists before creating
        self.user, created = User.objects.get_or_create(
            username=self.username,
            email=self.email,
            password=self.password
        )

        # Check if the test profile exists before creating
        if not hasattr(self.user, 'profile'):
            self.profile = Profile.objects.create(user=self.user)
        else:
            self.profile = self.user.profile

    def tearDown(self):
        """
        Clean up test user and profile.

        Deletes the test user and profile after each test.

        """
        if hasattr(self, 'user') and self.user is not None:
            self.user.delete()

        if hasattr(self, 'profile') and self.profile is not None:
            self.profile.delete()

    def test_user_profile_creation(self):
        """
        Test user profile creation.

        Ensures that a user profile is created successfully.

        """
        self.assertIsInstance(self.user.profile, Profile)
        self.assertEqual(str(self.user.profile), f"{self.user.username} Profile")


class UserRegistrationTestCase(TestCase):
    def test_user_register_view(self):
        """
        Test user registration view with valid data.

        Submits a registration form with valid data and checks if the user is created successfully.

        """
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword123', 'password2': 'newpassword123'}
        response = self.client.post(reverse('register'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account has been created! You are now able to login', html=True)
        self.assertTemplateUsed(response, 'users/login.html')

        new_user = User.objects.get(username='newuser')
        self.assertIsNotNone(new_user, 'User should have been created')

    def test_invalid_user_register_view(self):
        """
        Test user registration view with invalid data.

        Submits a registration form with invalid data and checks for error messages.

        """
        data = {'username': 'newuser', 'email': 'invalidemail', 'password1': 'newpassword123', 'password2': 'newpassword123'}
        response = self.client.post(reverse('register'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        form = response.context['form']
        self.assertIsInstance(form, UserRegisterForm)
        self.assertIn('Enter a valid email address.', form.errors['email'][0])

    def test_messages_after_registration(self):
        """
        Test success message after user registration.

        Submits a registration form and checks if the success message is displayed.

        """
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword123', 'password2': 'newpassword123'}
        response = self.client.post(reverse('register'), data, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your account has been created! You are now able to login')


class UserFormsTestCase(TestCase):
    def setUp(self):
        """
        Set up test data for user form tests.

        Creates a test user for testing user and profile forms.

        """
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_user_update_form(self):
        """
        Test user update form.

        Submits a user update form with valid data and checks if the form is valid.

        """
        form_data = {'username': 'newusername', 'email': 'newemail@example.com'}
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_update_form(self):
        """
        Test profile update form.

        Submits a profile update form with invalid data and checks for errors.

        """
        form_data = {}
        file_data = {'image': SimpleUploadedFile("test_image.jpg", content=b"file_content", content_type="image/jpeg")}
        form = ProfileUpdateForm(data=form_data, files=file_data, instance=self.user.profile)
        self.assertFalse(form.is_valid())  # Expecting form to be invalid
        self.assertIn('Upload a valid image.', form.errors['image'][0])
