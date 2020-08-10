from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    """ serializer for tag objects """

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'color',)
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
        fields = ('id', 'name', 'image')
        read_only_fields = ('id', 'name')


class FeedImageSerializer(serializers.ModelSerializer):
    """ serializer feed image """

    class Meta:
        model = models.FeedImage
        fields = ('id', 'image')
        read_only_fields = ('id',)


class FeedSerializer(serializers.ModelSerializer):
    """ serializer for feed object """
    tags = TagSerializer(many=True, read_only=True)
    user = UserFeedSerializer(read_only=True)
    like_status = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    image_feed = FeedImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Feed
        fields = ('id', 'user', 'feed', 'lat', 'long', 'tags',
                  'category', 'image_feed', 'location_lat',
                  'location_long', 'location_name', 'like_status',
                  'like_count', 'comment_count', 'date')
        read_only_fields = ('id', 'like_status', 'like_count',
                            'comment_count')

    def get_comment_count(self, feed):
        """ get comment count """
        return models.Comment.objects.filter(feed=feed).count()

    def get_like_count(self, feed):
        """ get like count """
        return models.Like.objects.filter(feed=feed).count()

    def get_like_status(self, feed):
        """ get the like status for feed """
        if self.context['request'].user.is_authenticated:
            the_user = self.context['request'].user
            likes = models.Like.objects.filter(user=the_user, feed=feed)
            if likes:
                return True

        return False


class FeedCreateSerializer(FeedSerializer):
    """ seralizer for creating feed """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )
    image_feed = serializers.ListSerializer(
        child=serializers.ImageField(
            allow_empty_file=False,
            max_length=100000
        ),
        required=False
    )

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        images_data = validated_data.pop('image_feed', [])
        feed = models.Feed.objects.create(**validated_data)

        for tag in tags_data:
            tags, created = models.Tag.objects.get_or_create(name=tag)
            feed.tags.add(tag)

        for image in images_data:
            models.FeedImage.objects.create(feed=feed, image=image)

        return feed


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
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = models.Community
        fields = ('id', 'name', 'subtitle', 'lat', 'long',
                  'description', 'location', 'image', 'is_joined',)
        read_only_fields = ('id', 'name', 'subtitle', 'lat', 'long')

    def get_is_joined(self, community):
        """ get is joined community status """
        if self.context['request'].user.is_anonymous:
            return False
            
        the_user = self.context['request'].user
        joined = models.CommunityMember.objects.filter(
            user=the_user,
            community=community,
            is_joined=True
        )

        if joined:
            return True
        
        return False


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


class DiscussionImageSerializer(serializers.ModelSerializer):
    """ discussion image serializer """
    class Meta:
        model = models.DiscussionImage
        fields = ('id', 'image')
        read_only_fields = ('id',)


class DiscussionLikeSerializer(serializers.ModelSerializer):
    """ serializer for discussion like """

    class Meta:
        model = models.DiscussionLike
        fields = ('id', 'user', 'discussion')
        read_only_fields = ('id', 'user')


class DiscussionSerializer(serializers.ModelSerializer):
    """ serializer for community discussion """
    user = UserFeedSerializer(read_only=True)
    like_status = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    discussion_image = DiscussionImageSerializer(many=True, read_only=True)
    like = serializers.SerializerMethodField()

    class Meta:
        model = models.CommunityDiscussion
        fields = ('id', 'user', 'community', 'text', 'like', 'date',
                  'discussion_image', 'like_status', 'like_count',
                  'comment_count')
        read_only_fields = ('id', 'user', 'like')

    def get_comment_count(self, disc):
        """ get comment count """
        return models.DiscussionComment.objects.filter(discussion=disc).count()

    def get_like_count(self, disc):
        """ get like count """
        return models.DiscussionLike.objects.filter(discussion=disc).count()

    def get_like_status(self, disc):
        """ get the like status for feed """
        the_user = self.context['request'].user
        likes = models.DiscussionLike.objects.filter(
            user=the_user,
            discussion=disc
        )
        if likes:
            return True

        return False

    def get_like(self, disc):
        the_user = self.context['request'].user
        likes = models.DiscussionLike.objects.filter(user=the_user, discussion=disc)
        serializer = DiscussionLikeSerializer(instance=likes, many=True)
        obj = serializer.data[0]
        return obj


class DiscussionCreateSerializer(DiscussionSerializer):
    """ discussion create serializer """
    discussion_image = serializers.ListSerializer(
        child=serializers.ImageField(
            allow_empty_file=False,
            max_length=100000
        ),
        required=False
    )

    def create(self, validated_data):
        images_data = validated_data.pop('discussion_image', [])
        diss = models.CommunityDiscussion.objects.create(**validated_data)
        for image in images_data:
            models.DiscussionImage.objects.create(
                discussion=diss,
                image=image
            )

        return diss


class DiscussionCommentSerializer(serializers.ModelSerializer):
    """ serializer for discussion  comment """
    user = UserFeedSerializer(read_only=True)

    class Meta:
        model = models.DiscussionComment
        fields = ('id', 'user', 'discussion', 'comment', 'date')
        read_only_fields = ('id', 'user')
