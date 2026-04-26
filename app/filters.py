import django_filters
from .models import UserModel, Channel, Video, Comment, Playlist


class ChannelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Channel name')

    class Meta:
        model = Channel
        fields = []


class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label='Description')

    channel = django_filters.ModelChoiceFilter(queryset=Channel.objects.all(), label='Channel')

    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', label='Uploaded after')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', label='Uploaded before')

    class Meta:
        model = Video
        fields = []


class CommentFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains', label='Text')
    author = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(), label='Author')

    class Meta:
        model = Comment
        fields = []


class PlaylistFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    owner = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(), label='Owner')

    class Meta:
        model = Playlist
        fields = []