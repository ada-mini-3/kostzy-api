from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kostzy import views


router = DefaultRouter()
router.register('feeds', views.FeedsViewSet)

app_name = 'kostzy'

urlpatterns = [
    path('', include(router.urls))
]
