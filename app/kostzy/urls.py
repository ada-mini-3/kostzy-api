from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kostzy import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('feeds', views.FeedsViewSet)
router.register('likes', views.LikeViewSet)
router.register('comments', views.CommentViewSet)
router.register('community', views.CommunityViewSet)
router.register('discussion', views.DiscussionViewSet)
router.register('discussion-comment', views.DiscussionCommentViewSet)
router.register('discussion-like', views.DiscussionLikeViewSet)

app_name = 'kostzy'

urlpatterns = [
    path('', include(router.urls)),
]
