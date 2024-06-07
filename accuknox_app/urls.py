from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [

    # simple jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('user_registration_api/', views.user_registration_api, name='user_registration_api'),
    path('login_view/', views.login_view, name='login_view'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/', views.reject_friend_request, name='reject_friend_request'),


    path('list_friends/', views.list_friends, name='list_friends'),
    path('list_pending_requests/', views.list_pending_requests, name='list_pending_requests'),


]