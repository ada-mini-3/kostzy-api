from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """ test models """

    def test_create_user_with_email_success(self):
        """ test creating user with email is success """
        email = "rais@gmail.com"
        password = "testing123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalized_email(self):
        """ test creating user with normalized email """
        email = 'rais@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test112')

        self.assertEqual(user.email, email.lower())

    def test_create_new_user_invalid_email(self):
        """ test create user with invalid credentials """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
