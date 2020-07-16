from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag, Category, Feed, Like

from kostzy.serializers import FeedSerializer, LikeSerializer


URL_FEEDS = reverse('kostzy:feed-list')
URL_LIKES = reverse('kostzy:like-list')


def detail_like_url(like_id):
    """ return like detail url """
    return reverse('kostzy:like-detail', args=[like_id])


def create_tags(name='Happy'):
    """ helper to create tags """
    return Tag.objects.create(name=name)


def create_category(name='Information'):
    """ helper to create category """
    return Category.objects.create(name=name)


def create_feeds(user, **params):
    """ helper to create feeds """
    defaults = {
        'feed': 'Sample Feed',
        'lat': 5.00,
        'long': 3.00,
    }
    defaults.update(params)
    return Feed.objects.create(user=user, **defaults)


class PublicFeedApiTest(TestCase):
    """ test public feed api """
    def setUp(self):
        self.client = APIClient()
        self.sample_user = get_user_model().objects.create_user(
            email='test123@gmail.com',
            password='1234567'
        )

    def test_retrive_list_of_feeds(self):
        """ test retrieve basic list of feeds """
        category1 = create_category()
        category2 = create_category(name='Food')
        create_feeds(
            user=self.sample_user,
            feed='Hello',
            category=category1
        )
        create_feeds(user=self.sample_user, category=category2)

        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)

        res = self.client.get(URL_FEEDS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_list_of_feeds_filtered_category(self):
        """" test retrieve filtered feeds by category """
        category1 = create_category()
        category2 = create_category(name='Food')
        feeds1 = create_feeds(user=self.sample_user, category=category1)
        feeds2 = create_feeds(
            user=self.sample_user,
            feed='Kuy Makan',
            category=category2
        )

        res = self.client.get(URL_FEEDS, {
            'category': f'{category2.id}'
        })

        serializer1 = FeedSerializer(feeds1)
        serializer2 = FeedSerializer(feeds2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_retrieve_list_of_feeds_filtered_tags(self):
        """ test retrieve filtered feeds by tags """
        tag1 = create_tags()
        tag2 = create_tags(name='Happy')
        tag3 = create_tags(name='Gloom')
        category = create_category()
        feeds1 = create_feeds(user=self.sample_user, category=category)
        feeds2 = create_feeds(
            user=self.sample_user,
            feed='Kuy Makan',
            category=category
        )
        feeds1.tags.add(tag1)
        feeds1.tags.add(tag2)
        feeds2.tags.add(tag3)

        res = self.client.get(URL_FEEDS, {
            'tags': f'{tag1.id}'
        })

        serializer1 = FeedSerializer(feeds1)
        serializer2 = FeedSerializer(feeds2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_feed_restricted(self):
        """test that create feed is restricted to authorized user"""
        res = self.client.post(URL_FEEDS, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFeedsApiTest(TestCase):
    """ private feeds api test """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='testing123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_feeds_is_successful(self):
        """ test that create feeds is successful """
        category = create_category()
        payload = {
            'feed': 'New Feeds',
            'category': category.id,
            'lat': 7,
            'long': 10
        }

        res = self.client.post(URL_FEEDS, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_feeds_with_tags(self):
        """ test create feed with tags is successful """
        category = create_category()
        tag1 = create_tags()
        tag2 = create_tags(name='Happy')
        payload = {
            'feed': 'New Feeds',
            'category': category.id,
            'lat': 7,
            'long': 10,
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(URL_FEEDS, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        feed = Feed.objects.get(id=res.data['id'])
        tags = feed.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_feeds_with_invalid_credentials(self):
        """ test create feed invalid credentials failed """
        res = self.client.post(URL_FEEDS, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_feeds_like(self):
        """ test create like in feeds"""
        category = create_category()
        feeds = create_feeds(user=self.user, category=category)

        payload = {'feed': feeds.id}

        res = self.client.post(URL_LIKES, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_feeds_unlike(self):
        """ test unlike feeds """
        category = create_category()
        feeds = create_feeds(user=self.user, category=category)
        like = Like.objects.create(user=self.user, feed=feeds)
        url = detail_like_url(like.id)
        res = self.client.delete(url)

        likes = Like.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(likes.count(), 0)

    def test_get_likes(self):
        """ test get likes """
        category = create_category()
        feeds = create_feeds(user=self.user, category=category, feed='Hello')
        feeds = create_feeds(user=self.user, category=category)
        Like.objects.create(user=self.user, feed=feeds)
        Like.objects.create(user=self.user, feed=feeds)

        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)

        res = self.client.get(URL_LIKES)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
