from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path


from .views import user_register, user_login, profile_view, logout_view, follow_view


app_name = "members"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<int:pk>/', follow_view, name='follow')
     
]