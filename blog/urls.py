from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>', views.delete_com, name='delete_com'),

    
]

