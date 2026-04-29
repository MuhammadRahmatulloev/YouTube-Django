from django.urls import path
from .views import (
    HomeView, ProfileView, ProfileUpdateView, DeleteAccountView, RestoreRequestView,
    register_view, verify_otp_view, login_view, logout_view,
    reset_request_view, reset_verify_otp_view, reset_new_password_view,
    change_password_view,
    ChannelCreateView, ChannelDetailView, ChannelUpdateView, SubscribeToggleView,
    VideoCreateView, VideoDetailView, VideoUpdateView, VideoDeleteView,
    LikeToggleView, CommentCreateView, CommentDeleteView,
    PlaylistListView, PlaylistCreateView, PlaylistDetailView, PlaylistDeleteView,
    PlaylistAddVideoView, PlaylistRemoveVideoView,
    AdminDashboardView,
    AdminSoftDeleteUserView, AdminRestoreUserView, AdminHardDeleteUserView,
    AdminSoftDeleteVideoView, AdminRestoreVideoView, AdminHardDeleteVideoView,
    AdminApproveRestoreRequestView, AdminRejectRestoreRequestView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),

    path('register/', register_view, name='register'),
    path('verify/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('restore-account/', RestoreRequestView.as_view(), name='restore_request'),

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

    path('admin-panel/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-panel/users/<int:pk>/deactivate/', AdminSoftDeleteUserView.as_view(), name='admin_soft_delete_user'),
    path('admin-panel/users/<int:pk>/restore/', AdminRestoreUserView.as_view(), name='admin_restore_user'),
    path('admin-panel/users/<int:pk>/delete/', AdminHardDeleteUserView.as_view(), name='admin_hard_delete_user'),
    path('admin-panel/videos/<int:pk>/remove/', AdminSoftDeleteVideoView.as_view(), name='admin_soft_delete_video'),
    path('admin-panel/videos/<int:pk>/restore/', AdminRestoreVideoView.as_view(), name='admin_restore_video'),
    path('admin-panel/videos/<int:pk>/delete/', AdminHardDeleteVideoView.as_view(), name='admin_hard_delete_video'),
    path('admin-panel/requests/<int:pk>/approve/', AdminApproveRestoreRequestView.as_view(), name='admin_approve_request'),
    path('admin-panel/requests/<int:pk>/reject/', AdminRejectRestoreRequestView.as_view(), name='admin_reject_request'),
]