from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    path('register/', register_view, name='register'),
    path('verify/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('reset/', reset_request_view, name='reset_request'),
    path('reset/verify/', reset_verify_otp_view, name='reset_verify_otp'),
    path('reset/new-password/', reset_new_password_view, name='reset_new_password'),

    path('change-password/', change_password_view, name='change_password'),

    path('channels/create/', ChannelCreateView.as_view(), name='channel_create'),
    path('channels/<int:pk>/', ChannelDetailView.as_view(), name='channel_detail'),
    path('channels/<int:pk>/update/', ChannelUpdateView.as_view(), name='channel_update'),
    path('channels/<int:channel_pk>/subscribe/', SubscribeToggleView.as_view(), name='subscribe_toggle'),

    path('videos/create/', VideoCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('videos/<int:pk>/update/', VideoUpdateView.as_view(), name='video_update'),
    path('videos/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
    path('videos/<int:video_pk>/like/', LikeToggleView.as_view(), name='like_toggle'),
    path('videos/<int:video_pk>/comment/', CommentCreateView.as_view(), name='comment_create'),

    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('playlists/', PlaylistListView.as_view(), name='playlist_list'),
    path('playlists/create/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlists/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlists/<int:playlist_pk>/add/<int:video_pk>/', PlaylistAddVideoView.as_view(), name='playlist_add_video'),
    path('playlists/<int:playlist_pk>/remove/<int:video_pk>/', PlaylistRemoveVideoView.as_view(), name='playlist_remove_video'),
]