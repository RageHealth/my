from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path


from .views import user_register, user_login, user_profile, logout_view


app_name = "members"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/<str:username>/', user_profile, name='profile'),
]