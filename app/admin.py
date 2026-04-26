from django.contrib import admin
from .models import UserModel, Channel, Video, Comment, Like, Subscription, Playlist

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'channel', 'views_count', 'is_published', 'created_at')
    search_fields = ('title', 'channel__name')
    list_filter = ('is_published',)
    list_editable = ('is_published',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'video', 'created_at')
    search_fields = ('author__username', 'video__title')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'is_like')
    list_filter = ('is_like',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'channel', 'created_at')
    search_fields = ('subscriber__username', 'channel__name')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_public', 'created_at')
    search_fields = ('title', 'owner__username')
    list_filter = ('is_public',)