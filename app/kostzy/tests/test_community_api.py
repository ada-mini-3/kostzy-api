# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# from core.models import Community, CommunityMember

# from kostzy.serializers import CommunityRetrieveSerializer


# URL_COMMUNITY = reverse('kostzy:community-list')


# class CommunityApiTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             email='raisazka@gmail.com',
#             password='testing123'
#         )
#         self.client.force_authenticate(user=self.user)
#         self.community = Community.objects.create(
#             name='Sample Kost',
#             lat=10,
#             long=5,
#             description='Kost area binus',
#             subtitle='Subtitle',
#             location='Binus'
#         )

#     def test_get_all_community(self):
#         """ test get community successful """
#         res = self.client.get(URL_COMMUNITY)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         communities = Community.objects.all()
#         self.assertEqual(len(communities), 1)

#     def test_retrieve_community(self):
#         """ test retrieve community successful """
#         url = reverse('kostzy:community-detail', args=[self.community.id])
#         res = self.client.get(url)

#         serializer = CommunityRetrieveSerializer(self.community)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_member_request_community(self):
#         """ test member request to join community """
#         comm_id = self.community.id
#         url = reverse('kostzy:community-member-request', args=[comm_id])

#         res = self.client.post(url)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         members = CommunityMember.objects.all()
#         self.assertEqual(len(members), 1)
