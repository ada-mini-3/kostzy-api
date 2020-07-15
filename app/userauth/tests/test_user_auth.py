from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


URL_REGISTER = reverse('userauth:register')
URL_LOGIN = reverse('userauth:login')
URL_PROFILE = reverse('userauth:profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AuthApiTest(TestCase):
    """ test login and register """

    def setUp(self):
        self.client = APIClient()

    def test_user_register(self):
        """ test user register with valid credentials """

        payload = {
            'name': 'Rais',
            'email': 'raisazka@gmail.com',
            'password': 'test123'
        }

        res = self.client.post(URL_REGISTER, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', res.data)

    def test_user_register_user_exists(self):
        """ test user register with user already exists """
        payload = {
            'name': 'Rais',
            'email': 'raisazka@gmail.com',
            'password': 'test123'
        }
        create_user(**payload)

        res = self.client.post(URL_REGISTER, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_invalid_credentials(self):
        """ test user register with invalid credentials """
        payload = {'email': '', 'password': 'testing123'}

        res = self.client.post(URL_REGISTER, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """ test user login successful """
        payload = {'email': 'rais@gmail.com', 'password': 'testing1234'}
        create_user(**payload)
        res = self.client.post(URL_LOGIN, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_user_login_invalid_credentials(self):
        """ test user login with invalid credentials """
        payload = {'email': 'rais@gmail.com', 'password': ''}

        res = self.client.post(URL_LOGIN, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_user_login_without_account(self):
        """ test user login without valid account """
        payload = {'email': 'rais@gmail.com', 'password': 'testing1234'}

        res = self.client.post(URL_LOGIN, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_user_cant_access_profile_without_login(self):
        """ test user cannot access profile without
            token credentials """
        res = self.client.get(URL_PROFILE)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileApiTest(TestCase):
    """ test user profile api """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='raisazka@gmail.com',
            name='Rais',
            password='testing123'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile_success(self):
        """ test return user profile is successful """
        res = self.client.get(URL_PROFILE)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)

    def test_update_user_profile_success(self):
        """ test update user profile is success """
        payload = {
            'name': 'New Name',
            'password': 'New Pass',
            'about': 'New About'
        }

        res = self.client.patch(URL_PROFILE, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.about, payload['about'])
        self.assertTrue(self.user.check_password(payload['password']))

    def test_profile_post_method_not_allowed(self):
        """ test that post method not allowed in profile url """
        res = self.client.post(URL_PROFILE, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
