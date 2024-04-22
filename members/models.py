from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    tiktokurl = models.URLField(blank=True)
    youtubeurl = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    shapka = models.ImageField(upload_to='shapki/', blank=True)

    def __str__(self):
        return self.user.username