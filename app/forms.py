from django import forms
from .models import UserModel, Channel, Video, Comment, Playlist


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. john_doe'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. john@gmail.com'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })
    )


class ChannelForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label="Channel Name",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. My Awesome Channel'
        })
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input form-textarea',
            'rows': 5,
            'placeholder': 'Tell viewers about your channel...'
        })
    )
    avatar = forms.ImageField(
        label="Channel Avatar",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-file'})
    )

    class Meta:
        model = Channel
        fields = ['name', 'description', 'avatar']


class VideoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. My First Video'
        })
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input form-textarea',
            'rows': 5,
            'placeholder': 'Describe your video...'
        })
    )
    video_file = forms.FileField(
        label="Video File",
        widget=forms.ClearableFileInput(attrs={'class': 'form-file'})
    )
    thumbnail = forms.ImageField(
        label="Thumbnail",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-file'})
    )
    is_published = forms.BooleanField(
        label="Publish immediately",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'is_published']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="Comment",
        widget=forms.Textarea(attrs={
            'class': 'form-input form-textarea',
            'rows': 3,
            'placeholder': 'Write a comment...'
        })
    )

    class Meta:
        model = Comment
        fields = ['text']


class PlaylistForm(forms.ModelForm):
    title = forms.CharField(
        max_length=150,
        label="Playlist Name",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. My Favorites'
        })
    )
    is_public = forms.BooleanField(
        label="Make public",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    class Meta:
        model = Playlist
        fields = ['title', 'is_public']


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        label="Profile Photo",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control tt-input'})
    )
    bio = forms.CharField(
        label="Bio",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control tt-input tt-textarea',
            'rows': 3,
            'placeholder': 'Tell something about yourself...'
        })
    )

    class Meta:
        model = UserModel
        fields = ['avatar', 'bio']