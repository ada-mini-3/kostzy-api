from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from kostzy.serializers import FeedSerializer
from core.models import Feed


class FeedsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):

    serializer_class = FeedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
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

        return queryset

    def perform_create(self, serializer):
        """ save the feed with user id """
        serializer.save(user=self.request.user)
