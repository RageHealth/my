import profile
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404




class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    tiktokurl = models.URLField(blank=True)
    youtubeurl = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    shapka = models.ImageField(upload_to='shapki/', blank=True)

    followers = models.ManyToManyField('self', symmetrical=False, related_name="following", blank=True)

    def follow(self,profile):
        self.followers.add(profile)

    def unfollow(self,profile):
        self.followers.remove(profile)

    def is_following(self, profile):
        return profile in self.followers.all()
    
    def get_followers(self):
        return self.followers.all()
    
    def get_following(self):
        return Profile.objects.filter(followers=self)
        


    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    profile = models.ForeignKey('auth.User', related_name='notification', on_delete=models.CASCADE)
    message = models.TextField()
    url = models.URLField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.notification_type
    
    def get_icon(self):
        if self.notification_type == 'like':
            return 'heart'
        elif self.notification_type == 'comment':
            return 'comment'
        elif self.notification_type == 'follow':
            return 'user-friends'
    
    def add_like(self,post,author_like):
        self.notification_type = 'like'
        self.profile = post.author
        self.message = '{} liked your post'.format(author_like.username)
        self.url = '/posts/{}/'.format(post.pk)
        self.save()

    def add_comment(self,post,author_comment):
        self.notification_type = 'comment'
        self.profile = post.author
        self.message = '{} commented your post'.format(author_comment.username)
        self.url = '/posts/{}/'.format(post.pk)
        self.save()

    def add_follow(self,post,author_follow):
        self.notification_type = 'follow'
        self.profile = profile
        self.message = '{} started following you'.format(author_follow.username)
        self.url = '/posts/{}/'.format(author_follow.profile.pk)
        self.save()

    def read(self):
        self.is_read = True
        self.save()