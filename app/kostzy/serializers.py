from rest_framework import serializers

from core.models import Tag, Category, Feed, User


class TagSerializer(serializers.ModelSerializer):
    """ serializer for tag objects """

    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """ serializer for category objects """

    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class UserFeedSerializer(serializers.ModelSerializer):
    """ serializer for user obj in feeds"""

    class Meta:
        model = User
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class FeedSerializer(serializers.ModelSerializer):
    """ serializer for feed object """
    tags = TagSerializer(many=True, read_only=True)
    user = UserFeedSerializer(read_only=True)

    class Meta:
        model = Feed
        fields = ('id', 'user', 'feed', 'lat', 'long', 'tags',
                  'category', 'location_lat', 'location_long')
        read_only_fields = ('id',)
