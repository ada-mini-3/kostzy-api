from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import CommunityDiscussion, Community

from kostzy.serializers import DiscussionSerializer


URL_DISCUSSION = 'http://127.0.0.1:8000/api/v1/discussion/'


class DiscussionApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='testing123'
        )
        self.client.force_authenticate(user=self.user)
        self.community = Community.objects.create(
            name='Sample Kost',
            lat=10,
            long=5,
            description='Kost area binus',
            subtitle='Subtitle',
            location='Binus'
        )

    def test_get_discussion_from_certain_community(self):
        """ test getting discussion in a certain community id """
        comm2 = Community.objects.create(
            name='Sample Kost 2',
            lat=10,
            long=5,
            description='Kost area KG',
            subtitle='Subtitle',
            location='kemanggisan'
        )
        disscuss1 = CommunityDiscussion.objects.create(
            user=self.user,
            community=self.community,
            text='Hello'
        )
        disscuss2 = CommunityDiscussion.objects.create(
            user=self.user,
            community=comm2,
            text='Hello 2'
        )

        res = self.client.get(URL_DISCUSSION, {
                'community': f'{self.community.id}'
            }
        )
        serializer1 = DiscussionSerializer(disscuss1)
        serializer2 = DiscussionSerializer(disscuss2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_discussion_in_community(self):
        """ test create discussion in certain community """
        payload = {'community': self.community.id, 'text': 'Jancok'}

        res = self.client.post(URL_DISCUSSION, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        discussion = CommunityDiscussion.objects.all()
        self.assertEqual(len(discussion), 1)
