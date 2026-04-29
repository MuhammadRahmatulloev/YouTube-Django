from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email_token = models.UUIDField(default=uuid.uuid4)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    reset_token = models.UUIDField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()

    def __str__(self):
        return f'{self.username} - {self.email}'


class Channel(models.Model):
    owner = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='channel_avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()

    def __str__(self):
        return f'{self.title} - {self.channel}'


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.video}'


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    def __str__(self):
        return f'{self.user} - {self.video}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subscriber} - {self.channel}'


class Playlist(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    videos = models.ManyToManyField(Video, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.owner}'


class RestoreRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    email = models.EmailField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.status}'