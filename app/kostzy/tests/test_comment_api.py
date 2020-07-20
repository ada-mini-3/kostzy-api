# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# from core.models import Comment, Feed, Category

# from kostzy.serializers import CommentSerializer


# URL_COMMENT = reverse('kostzy:comment-list')


# def create_feeds(user, **params):
#     """ helper to create feeds """
#     category = Category.objects.create(name='Food')
#     defaults = {
#         'feed': 'Sample Feed',
#         'lat': 5.00,
#         'long': 3.00,
#         'category_id': category.id
#     }
#     defaults.update(params)
#     return Feed.objects.create(user=user, **defaults)


# class CommentApiTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             email='raisazka@gmail.com',
#             password='testing123'
#         )
#         self.client.force_authenticate(user=self.user)
#         self.feeds = create_feeds(user=self.user)

#     def test_get_comment_from_certain_feeds(self):
#         """ test get comment from certain feeds id """
#         comments = Comment.objects.create(
#             user=self.user,
#             feed=self.feeds,
#             comment='Sample Comment'
#         )

#         feeds2 = create_feeds(user=self.user)
#         comments2 = Comment.objects.create(
#             user=self.user,
#             feed=feeds2,
#             comment='Sample Comment'
#         )

#         res = self.client.get(URL_COMMENT, {'feed': f'{self.feeds.id}'})

#         serializer1 = CommentSerializer(comments)
#         serializer2 = CommentSerializer(comments2)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn(serializer1.data, res.data)
#         self.assertNotIn(serializer2.data, res.data)

#     def test_create_comment_is_successful(self):
#         """ test create comment is success """
#         payload = {'comment': 'Hellow', 'feed': self.feeds.id}

#         res = self.client.post(URL_COMMENT, payload)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         comments = Comment.objects.all()
#         self.assertEqual(len(comments), 1)
