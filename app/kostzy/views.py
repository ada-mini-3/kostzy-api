from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers

from kostzy import serializers
from core import models
from django.shortcuts import get_object_or_404

class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin):
    
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class FeedsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):

    serializer_class = serializers.FeedSerializer
    authentication_classes = (TokenAuthentication,)
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Feed.objects.all().order_by('-date')

    def get_queryset(self):
        """ retrieve & filter the feed """
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')
        queryset = self.queryset

        if tags:
            tag_id = tags
            queryset = queryset.filter(tags__id__in=tag_id)
        if category:
            cat_id = category
            queryset = queryset.filter(category=cat_id)

        return queryset.all()

    def perform_create(self, serializer):
        """ save the feed with user id """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """ return appropriate serializer class """
        if self.action == 'create':
            return serializers.FeedCreateSerializer
        else:
            return serializers.FeedSerializer


class LikeViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):

    serializer_class = serializers.LikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Like.objects.all()

    def perform_create(self, serializer):
        """ save the like with user id """
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):

    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Comment.objects.all().order_by('-date')

    def get_queryset(self):
        """ get comment based on feeds """
        feed_id = self.request.query_params.get('feed')
        return self.queryset.filter(feed=feed_id)

    def perform_create(self, serializer):
        """ save with user id """
        serializer.save(user=self.request.user)


class CommunityViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):

    serializer_class = serializers.CommunityListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Community.objects.all()

    def get_serializer_class(self):
        """ return appropriate serializer class """
        if self.action == 'list':
            return serializers.CommunityListSerializer
        elif self.action == 'retrieve':
            return serializers.CommunityRetrieveSerializer
        elif self.action == 'member_request':
            return serializers.CommunityMemberSerializer

    def perform_create(self, serializer):
        """ save with user id """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='member-request')
    def member_request(self, request, pk=None):
        """ member request join action """
        community = self.get_object()
        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(user=self.request.user, community=community)
            return Response(
                serializer.data,
                status.HTTP_201_CREATED
            )

        return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )


class DiscussionViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):

    serializer_class = serializers.DiscussionSerializer
    authentication_classes = (TokenAuthentication,)
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.CommunityDiscussion.objects.all().order_by('-date')

    def get_serializer_class(self):
        """ return appropriate serializer class """
        if self.action == 'create':
            return serializers.DiscussionCreateSerializer
        else:
            return serializers.DiscussionSerializer

    def get_queryset(self):
        """ return data based on community only """
        community_id = self.request.query_params.get('community')
        return self.queryset.filter(community__id=community_id)

    def perform_create(self, serializer):
        """ save with user id """
        return serializer.save(user=self.request.user)


class DiscussionCommentViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin):

    serializer_class = serializers.DiscussionCommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.DiscussionComment.objects.all().order_by('-date')

    def get_queryset(self):
        """ return only by discussion id """
        discussion_id = self.request.query_params.get('discussion')
        return self.queryset.filter(discussion__id=discussion_id)

    def perform_create(self, serializer):
        """ create new discussion comment with user id """
        serializer.save(user=self.request.user)


class DiscussionLikeViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin):

    serializer_class = serializers.DiscussionLikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.DiscussionLike.objects.all()

    def perform_create(self, serializer):
        """ create new discussion with user id """
        serializer.save(user=self.request.user)
