from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='raisazka@gmail.com',
            password='testing123'
        )
        """ log user to django auth """
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='usertest@gmail.com',
            password='testing123',
            name='Djancok'
        )

    def test_user_listed(self):
        """ test that user is listed """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_edit_page(self):
        """ test that user edit page is working """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """ test that user create page is working """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
