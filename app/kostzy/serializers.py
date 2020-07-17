from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    """ serializer for tag objects """

    class Meta:
        model = models.Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """ serializer for category objects """

    class Meta:
        model = models.Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class UserFeedSerializer(serializers.ModelSerializer):
    """ serializer for user obj in feeds"""

    class Meta:
        model = models.User
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class FeedSerializer(serializers.ModelSerializer):
    """ serializer for feed object """
    tags = TagSerializer(many=True, read_only=True)
    user = UserFeedSerializer(read_only=True)

    class Meta:
        model = models.Feed
        fields = ('id', 'user', 'feed', 'lat', 'long', 'tags',
                  'category', 'location_lat', 'location_long',
                  'location_name')
        read_only_fields = ('id',)


class FeedCreateSerializer(FeedSerializer):
    """ seralizer for creating feed """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )


class LikeSerializer(serializers.ModelSerializer):
    """ serializer for like object """

    class Meta:
        model = models.Like
        fields = ('id', 'user', 'feed', 'date',)
        read_only_fields = ('id', 'user',)


class CommentSerializer(serializers.ModelSerializer):
    """comment class serializer """

    user = UserFeedSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'user', 'feed', 'comment', 'date',)
        read_only_fields = ('id', 'user',)


class CommunityListSerializer(serializers.ModelSerializer):
    """ serializer for list community """

    class Meta:
        model = models.Community
        fields = ('id', 'name', 'subtitle', 'lat', 'long',)
        read_only_fields = ('id', 'name', 'subtitle', 'lat', 'long')


class CommunityRetrieveSerializer(serializers.ModelSerializer):
    """ serializer for retrieve community """

    class Meta:
        model = models.Community
        fields = ('id', 'name', 'description', 'lat', 'long', 'location',)
        read_only_fields = ('id', 'name', 'subtitle', 'lat',
                            'long', 'location')


class CommunityMemberSerializer(serializers.ModelSerializer):
    """ serializer for community member request join """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.CommunityMember
        fields = ('id', 'user', 'community', 'is_joined',)
        read_only_fields = ('id',)


class DiscussionSerializer(serializers.ModelSerializer):
    """ serializer for community discussion """

    class Meta:
        model = models.CommunityDiscussion
        fields = ('id', 'user', 'community', 'text')
        read_only_fields = ('id', 'user')
