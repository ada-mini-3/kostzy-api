from django.urls import path

from userauth import views


app_name = 'userauth'

urlpatterns = [
    path('register/', views.RegisterApiViewSet.as_view(
        {'post': 'create'}), name='register'),
    path('login/', views.LoginApiViewSet.as_view(), name='login'),
    path('profile/', views.ProfileApiViewSet.as_view(), name='profile')
]
