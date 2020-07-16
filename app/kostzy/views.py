from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

from kostzy import serializers
from core.models import Feed, Like, Comment


class FeedsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,):

    serializer_class = serializers.FeedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Feed.objects.all()

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
    queryset = Like.objects.all()

    def get_queryset(self):
        """ get likes for the authenticated user """
        feeds = Feed.objects.filter(user=self.request.user)
        return self.queryset.filter(feed__in=feeds)

    def perform_create(self, serializer):
        """ save the like with user id """
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):

    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()

    def get_queryset(self):
        """ get comment based on feeds """
        feed_id = self.request.query_params.get('feed')
        return self.queryset.filter(feed=feed_id)

    def perform_create(self, serializer):
        """ save with user id """
        serializer.save(user=self.request.user)
