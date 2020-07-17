from rest_framework import serializers

from core.models import Tag, Category, Feed, User, Like, \
                        Comment, Community, CommunityMember


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
                  'category', 'location_lat', 'location_long',
                  'location_name')
        read_only_fields = ('id',)


class FeedCreateSerializer(FeedSerializer):
    """ seralizer for creating feed """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )


class LikeSerializer(serializers.ModelSerializer):
    """ serializer for like object """

    class Meta:
        model = Like
        fields = ('id', 'user', 'feed', 'date',)
        read_only_fields = ('id', 'user',)


class CommentSerializer(serializers.ModelSerializer):
    """comment class serializer """

    user = UserFeedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'feed', 'comment', 'date',)
        read_only_fields = ('id', 'user',)


class CommunityListSerializer(serializers.ModelSerializer):
    """ serializer for list community """

    class Meta:
        model = Community
        fields = ('id', 'name', 'subtitle', 'lat', 'long',)
        read_only_fields = ('id', 'name', 'subtitle', 'lat', 'long')


class CommunityRetrieveSerializer(serializers.ModelSerializer):
    """ serializer for retrieve community """

    class Meta:
        model = Community
        fields = ('id', 'name', 'description', 'lat', 'long', 'location',)
        read_only_fields = ('id', 'name', 'subtitle', 'lat',
                            'long', 'location')


class CommunityMemberSerializer(serializers.ModelSerializer):
    """ serializer for community member request join """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommunityMember
        fields = ('id', 'user', 'community', 'is_joined',)
        read_only_fields = ('id',)
