from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset-password/', reset_password, name='reset_password'),
    path('info/', info, name='info'),
    path('change-password/<str:id_hash>/', change_password, name='change_password')
]