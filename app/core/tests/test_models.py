from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Category, Feed, Like, \
                        Comment, Community, CommunityMember


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

    def test_tag_model(self):
        """ test tag models return name """
        tag = Tag.objects.create(
            name='Happy'
        )

        self.assertEqual(str(tag), tag.name)

    def test_category_model(self):
        """ test category model return name """
        category = Category.objects.create(
            name='Foods'
        )

        self.assertEqual(str(category), category.name)

    def test_feeds_model(self):
        """ test feed model return the feeds """
        user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='password123'
        )
        category = Category.objects.create(
            name='Foods'
        )
        feeds = Feed.objects.create(
            user=user,
            category=category,
            feed='Hello',
            lat=10,
            long=16
        )

        self.assertEqual(str(feeds), feeds.feed)

    def test_like_model(self):
        """ test like model """
        user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='password123'
        )
        category = Category.objects.create(
            name='Foods'
        )
        feeds = Feed.objects.create(
            user=user,
            category=category,
            feed='Hello',
            lat=10,
            long=16
        )

        like = Like.objects.create(user=user, feed=feeds)

        self.assertEqual(str(like), like.feed.feed)

    def test_comments_model(self):
        """ test comment model """
        user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='password123'
        )
        category = Category.objects.create(
            name='Foods'
        )
        feeds = Feed.objects.create(
            user=user,
            category=category,
            feed='Hello',
            lat=10,
            long=16
        )

        comments = Comment.objects.create(
            user=user,
            feed=feeds,
            comment='The New Comment',
        )

        self.assertEqual(str(comments), comments.comment)

    def test_community_model(self):
        """ test community model return name """
        community = Community.objects.create(
            name='Sample Kost',
            lat=10,
            long=5,
            description='Kost area binus',
            subtitle='Subtitle',
            location='Binus'
        )

        self.assertEqual(str(community), community.name)

    def test_community_member_model(self):
        """ test community member model """
        user = get_user_model().objects.create_user(
            email='raisazka@gmail.com',
            password='password123'
        )
        community = Community.objects.create(
            name='Sample Kost',
            lat=10,
            long=5,
            description='Kost area binus',
            subtitle='Subtitle',
            location='Binus'
        )
        comm_member = CommunityMember.objects.create(
            user=user,
            community=community
        )

        self.assertEqual(str(comm_member), community.name)
