from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

from kostzy import serializers
from core.models import Feed, Like


class FeedsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):

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
            queryset = queryset.filter(category__id__in=cat_id)

        return queryset.all()

    def perform_create(self, serializer):
        """ save the feed with user id """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """ return appropriate serializer class """
        if self.action == 'list':
            return serializers.FeedSerializer
        elif self.action == 'create':
            return serializers.FeedCreateSerializer


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
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ save the like with user id """
        serializer.save(user=self.request.user)
