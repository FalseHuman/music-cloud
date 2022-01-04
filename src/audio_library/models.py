from django.db import models
from django.core.validators import FileExtensionValidator
from src.oauth.models import AuthUser
from src.base.services import validate_size_image, get_upload_cover_albums, get_upload_tracks, get_upload_cover_playlist, get_upload_cover_tracks


class License(models.Model):
    """Модель лицензий треков"""
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="licenses")
    text = models.TextField(max_length=1000)


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Albums(models.Model):
    """Модель альбомов для треков"""
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(upload_to=get_upload_cover_albums, blank=True,
                              null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image])


class Track(models.Model):
    """Модель треков"""
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=100)
    license =models.ForeignKey(License, on_delete=models.PROTECT, related_name='license_tracks')
    genre = models.ManyToManyField(Genre,related_name='tracks_genres')
    album = models.ForeignKey(Albums, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_tracks, validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])#file
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    private = models.BooleanField(default=False)
    cover = models.ImageField(upload_to=get_upload_cover_tracks, blank=True,
                              null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image])
    user_of_likes = models.ManyToManyField(
        AuthUser,  related_name="likes_off_tracks")

    def __str__(self):
        return f'{self.user} - {self.title}'

class Comment(models.Model):
    """Модель комментариев пользователей"""
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="comments")
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name="track_comments")
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)

class PlayList(models.Model):
    """Модель плейлистов пользователя"""
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="play_lists")
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='track_play_lists')
    cover = models.ImageField(upload_to=get_upload_cover_playlist, blank=True,
                              null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image])
