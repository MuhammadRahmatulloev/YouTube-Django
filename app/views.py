from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
import random
from .models import UserModel, Channel, Video, Comment, Like, Subscription, Playlist
from .forms import RegisterForm, LoginForm, ChannelForm, VideoForm, CommentForm, PlaylistForm
from .permissions import SessionLoginRequiredMixin, OwnerOrAdminRequiredMixin
import os, re
from django.http import StreamingHttpResponse, FileResponse, HttpResponse
from django.conf import settings
from .forms import RegisterForm, LoginForm, ChannelForm, VideoForm, CommentForm, PlaylistForm, ProfileUpdateForm


# def serve_video_range(request, path):
#     video_path = os.path.join(settings.MEDIA_ROOT, path)
#     if not os.path.exists(video_path):
#         return HttpResponse(status=404)

#     file_size = os.path.getsize(video_path)
#     range_header = request.META.get('HTTP_RANGE', '')
#     content_type = 'video/mp4'

#     if range_header:
#         match = re.match(r'bytes=(\d+)-(\d*)', range_header)
#         if match:
#             start = int(match.group(1))
#             end = int(match.group(2)) if match.group(2) else file_size - 1
#             end = min(end, file_size - 1)
#             length = end - start + 1

#             def iterator(p, offset, size, chunk=65536):
#                 with open(p, 'rb') as f:
#                     f.seek(offset)
#                     remaining = size
#                     while remaining > 0:
#                         data = f.read(min(chunk, remaining))
#                         if not data:
#                             break
#                         remaining -= len(data)
#                         yield data

#             response = StreamingHttpResponse(
#                 iterator(video_path, start, length),
#                 status=206,
#                 content_type=content_type,
#             )
#             response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
#             response['Accept-Ranges'] = 'bytes'
#             response['Content-Length'] = length
#             return response

#     response = FileResponse(open(video_path, 'rb'), content_type=content_type)
#     response['Accept-Ranges'] = 'bytes'
#     response['Content-Length'] = file_size
#     return response


def serve_video_range(request, path):
    video_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(video_path):
        return HttpResponse(status=404)

    return FileResponse(open(video_path, 'rb'), content_type='video/mp4')


def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return UserModel.objects.filter(id=user_id).first()


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp, subject='TajTube — Verification Code', username=''):
    send_mail(
        subject=subject,
        message=(
            f'Hello{" " + username if username else ""}!\n\n'
            f'Your verification code is:\n\n'
            f'        {otp}\n\n'
            f'Enter this 6-digit code on the verification page.\n'
            f'The code is valid for one use only.\n\n'
            f'— TajTube Team'
        ),
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        if not all([username, email, password, confirm]):
            messages.error(request, 'Please fill in all fields!')
            return render(request, 'register.html')

        if password != confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        if UserModel.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken!')
            return render(request, 'register.html')

        if UserModel.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered!')
            return render(request, 'register.html')

        user = UserModel(username=username, email=email)
        user.set_password(password)
        otp = generate_otp()
        user.otp_code = otp
        user.save()

        request.session['pending_user_id'] = user.id

        try:
            send_otp_email(email=email, otp=otp, subject='TajTube — Email Verification', username=username)
        except Exception:
            messages.warning(request, f'Email could not be sent. Your OTP code: {otp}')

        return redirect('verify_otp')
    return render(request, 'register.html')


def verify_otp_view(request):
    pending_id = request.session.get('pending_user_id')
    if not pending_id:
        messages.error(request, 'No pending verification. Please register first.')
        return redirect('register')

    user = UserModel.objects.filter(id=pending_id).first()
    if not user:
        messages.error(request, 'User not found. Please register again.')
        return redirect('register')

    if request.method == 'POST':
        entered = request.POST.get('otp_code', '').strip()
        if entered == user.otp_code:
            user.is_active = True
            user.otp_code = None
            user.save()
            del request.session['pending_user_id']
            messages.success(request, 'Email verified! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid code. Please try again.')

    return render(request, 'verify_otp.html', {'email': user.email})


def login_view(request):
    if request.method != 'POST':
        return render(request, 'login.html')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    user = UserModel.objects.filter(username=username).first()

    if not user or not user.check_password(password):
        messages.error(request, 'Invalid username or password!')
        return render(request, 'login.html')

    if not user.is_active:
        messages.error(request, 'Please verify your email first!')
        return render(request, 'login.html')

    request.session['user_id'] = user.id
    messages.success(request, f'Welcome back, {user.username}!')
    return redirect('home')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = UserModel.objects.filter(email=email).first()

        if user:
            otp = generate_otp()
            user.otp_code = otp
            user.save()
            request.session['reset_email'] = email
            try:
                send_otp_email(email=email, otp=otp, subject='TajTube — Password Reset Code', username=user.username)
            except Exception:
                messages.warning(request, f'Email not sent. Your reset code: {otp}')

        messages.success(request, 'If this email exists — a reset code has been sent!')
        return redirect('reset_verify_otp')

    return render(request, 'reset_request.html')


def reset_verify_otp_view(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Session expired. Please request a reset again.')
        return redirect('reset_request')

    user = UserModel.objects.filter(email=email).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('reset_request')

    if request.method == 'POST':
        entered = request.POST.get('otp_code', '').strip()
        if entered == user.otp_code:
            user.otp_code = None
            user.save()
            request.session['reset_verified_id'] = user.id
            del request.session['reset_email']
            return redirect('reset_new_password')
        else:
            messages.error(request, 'Invalid code. Please try again.')

    return render(request, 'reset_verify_otp.html', {'email': email})


def reset_new_password_view(request):
    verified_id = request.session.get('reset_verified_id')
    if not verified_id:
        messages.error(request, 'Session expired. Please request a reset again.')
        return redirect('reset_request')

    user = UserModel.objects.filter(id=verified_id).first()
    if not user:
        return redirect('reset_request')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')

        if new_password != confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'reset_confirm.html')

        user.set_password(new_password)
        user.save()
        del request.session['reset_verified_id']
        messages.success(request, 'Password changed successfully! Please log in.')
        return redirect('login')

    return render(request, 'reset_confirm.html')


def change_password_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    if request.method == 'POST':
        old = request.POST.get('old', '')
        new = request.POST.get('new', '')
        confirm = request.POST.get('confirm', '')

        if not user.check_password(old):
            messages.error(request, 'Old password is incorrect!')
            return render(request, 'change_password.html')

        if new != confirm:
            messages.error(request, 'New passwords do not match!')
            return render(request, 'change_password.html')

        user.set_password(new)
        user.save()
        messages.success(request, 'Password updated successfully!')
        return redirect('login')

    return render(request, 'change_password.html')


class ProfileView(View):
    def get(self, request):
        user = get_current_user(request)
        if not user:
            messages.error(request, 'Please login first!')
            return redirect('login')
        channel = Channel.objects.filter(owner=user).first()
        subscriptions = Subscription.objects.filter(subscriber=user).select_related('channel')
        return render(request, 'profile.html', {
            'user': user,
            'channel': channel,
            'playlists': Playlist.objects.filter(owner=user),
            'subscriptions': subscriptions,
        })
    

class ProfileUpdateView(SessionLoginRequiredMixin, View):
    def get(self, request):
        user = get_current_user(request)
        form = ProfileUpdateForm(instance=user)
        return render(request, 'profile_update.html', {'form': form, 'user': user})

    def post(self, request):
        user = get_current_user(request)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
        return redirect('profile')


class HomeView(ListView):
    model = Video
    template_name = 'home.html'
    context_object_name = 'videos'

    def get_queryset(self):
        qs = Video.objects.filter(is_published=True).select_related('channel').order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_current_user(self.request)

        context['videos'] = (Video.objects.filter(channel=self.object, is_published=True).order_by('-created_at'))
        context['subscribers_count'] = (Subscription.objects.filter(channel=self.object).count())

        if user:
            context['is_subscribed'] = Subscription.objects.filter(subscriber=user, channel=self.object).exists()
        
        else:
            context['is_subscribed'] = False

        return context


class ChannelCreateView(SessionLoginRequiredMixin, CreateView):
    model = Channel
    template_name = 'channel_create.html'
    form_class = ChannelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = get_current_user(self.request)
        if Channel.objects.filter(owner=user).exists():
            messages.error(self.request, 'You already have a channel!')
            return redirect('home')
        form.instance.owner = user
        messages.success(self.request, 'Channel created successfully!')
        return super().form_valid(form)


class ChannelUpdateView(OwnerOrAdminRequiredMixin, UpdateView):
    model = Channel
    template_name = 'channel_update.html'
    form_class = ChannelForm
    context_object_name = 'channel'
    owner_field = 'owner'
    fail_redirect = 'home'

    def get_success_url(self):
        return reverse_lazy('channel_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Channel updated successfully!')
        return super().form_valid(form)


class VideoDetailView(DetailView):
    model = Video
    template_name = 'video_detail.html'
    context_object_name = 'video'

    def get_queryset(self):
        return Video.objects.select_related('channel').prefetch_related('comment_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_current_user(self.request)
        video = self.object

        video.views_count += 1
        video.save()

        context['comments'] = (
            Comment.objects.filter(video=video).select_related('author').order_by('-created_at'))
        context['comment_form'] = CommentForm()

        if user:
            context['user_like'] = Like.objects.filter(video=video, user=user).first()
            context['is_subscribed'] = Subscription.objects.filter(
                subscriber=user, channel=video.channel
            ).exists()
            context['playlists'] = Playlist.objects.filter(owner=user)
        else:
            context['user_like'] = None
            context['is_subscribed'] = False
            context['playlists'] = []

        context['likes_count'] = Like.objects.filter(video=video, is_like=True).count()
        context['dislikes_count'] = Like.objects.filter(video=video, is_like=False).count()

        return context


class VideoCreateView(SessionLoginRequiredMixin, CreateView):
    model = Video
    template_name = 'video_create.html'
    form_class = VideoForm

    def form_valid(self, form):
        user = get_current_user(self.request)
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            messages.error(self.request, 'You need to create a channel first!')
            return redirect('channel_create')
        form.instance.channel = channel
        messages.success(self.request, 'Video uploaded successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('video_detail', kwargs={'pk': self.object.pk})


class VideoUpdateView(OwnerOrAdminRequiredMixin, UpdateView):
    model = Video
    template_name = 'video_update.html'
    form_class = VideoForm
    context_object_name = 'video'
    owner_field = 'channel__owner'
    fail_redirect = 'home'

    def get_success_url(self):
        return reverse_lazy('video_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Video updated successfully!')
        return super().form_valid(form)


class VideoDeleteView(OwnerOrAdminRequiredMixin, DeleteView):
    model = Video
    template_name = 'video_delete.html'
    context_object_name = 'video'
    owner_field = 'channel__owner'
    fail_redirect = 'home'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Video deleted successfully!')
        return super().form_valid(form)


class CommentCreateView(SessionLoginRequiredMixin, View):
    def post(self, request, video_pk):
        user = get_current_user(request)
        video = get_object_or_404(Video, pk=video_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video  = video
            comment.author = user
            comment.save()
            messages.success(request, 'Comment added!')
        return redirect('video_detail', pk=video_pk)


class CommentDeleteView(SessionLoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_current_user(request)
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == user or user.is_admin:
            comment.delete()
            messages.success(request, 'Comment deleted!')
        else:
            messages.error(request, 'You cannot delete this comment!')
        return redirect('video_detail', pk=comment.video.pk)


class LikeToggleView(SessionLoginRequiredMixin, View):
    def post(self, request, video_pk):
        user = get_current_user(request)
        video = get_object_or_404(Video, pk=video_pk)
        is_like = request.POST.get('is_like') == 'True'
        like = Like.objects.filter(video=video, user=user).first()

        if like:
            if like.is_like == is_like:
                like.delete()
            else:
                like.is_like = is_like
                like.save()
        else:
            Like.objects.create(video=video, user=user, is_like=is_like)

        return redirect('video_detail', pk=video_pk)


class SubscribeToggleView(SessionLoginRequiredMixin, View):
    def post(self, request, channel_pk):
        user = get_current_user(request)
        channel = get_object_or_404(Channel, pk=channel_pk)
        subscription = Subscription.objects.filter(subscriber=user, channel=channel).first()

        if subscription:
            subscription.delete()
            messages.success(request, f'Unsubscribed from {channel.name}.')
        else:
            Subscription.objects.create(subscriber=user, channel=channel)
            messages.success(request, f'Subscribed to {channel.name}!')

        return redirect('channel_detail', pk=channel_pk)


class PlaylistListView(SessionLoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'playlist_list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        user = get_current_user(self.request)
        return Playlist.objects.filter(owner=user).prefetch_related('videos')


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = self.object.videos.select_related('channel')
        return context


class PlaylistCreateView(SessionLoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'playlist_create.html'
    form_class = PlaylistForm
    success_url = reverse_lazy('playlist_list')

    def form_valid(self, form):
        form.instance.owner = get_current_user(self.request)
        messages.success(self.request, 'Playlist created successfully!')
        return super().form_valid(form)


class PlaylistDeleteView(OwnerOrAdminRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'playlist_delete.html'
    context_object_name = 'playlist'
    owner_field = 'owner'
    fail_redirect = 'playlist_list'
    success_url = reverse_lazy('playlist_list')

    def form_valid(self, form):
        messages.success(self.request, 'Playlist deleted!')
        return super().form_valid(form)


class PlaylistAddVideoView(SessionLoginRequiredMixin, View):
    def post(self, request, playlist_pk, video_pk):
        user = get_current_user(request)
        playlist = get_object_or_404(Playlist, pk=playlist_pk, owner=user)
        video = get_object_or_404(Video, pk=video_pk)
        playlist.videos.add(video)
        messages.success(request, f'Video added to "{playlist.title}"!')
        return redirect('video_detail', pk=video_pk)


class PlaylistRemoveVideoView(SessionLoginRequiredMixin, View):
    def post(self, request, playlist_pk, video_pk):
        user = get_current_user(request)
        playlist = get_object_or_404(Playlist, pk=playlist_pk, owner=user)
        video = get_object_or_404(Video, pk=video_pk)
        playlist.videos.remove(video)
        messages.success(request, f'Video removed from "{playlist.title}"!')
        return redirect('playlist_detail', pk=playlist_pk)