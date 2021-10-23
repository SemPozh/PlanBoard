from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset-password/', reset_password, name='reset_password'),
    path('info/', info, name='info'),
    path('change-password/<str:id_hash>/', change_password, name='change_password'),
    path('my-plans/add-template/', add_template, name='add_template'),
    path('ajax_add_template/', ajax_add_template, name='ajax_add_template'),
    path('ajax_save_template/', csrf_exempt(ajax_save_template), name='ajax_save_template'),
    path('my-plans/', my_plans, name="my-plans"),
]