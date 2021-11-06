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
    path('my-plans/ajax_add_plan/', ajax_add_plan, name="ajax_add_plan"),
    path('my-plans/ajax_create_plan/', csrf_exempt(ajax_create_plan), name="ajax_create_plan"),
    path('my-plans/api_get_plans_by_template_id/', api_get_plans_by_template_id, name="api_get_plans_by_template_id"),
    path('my-plans/api_get_plan_data/', api_get_plan_data, name="api_get_plan_data"),
    path('my-plans/ajax_redact_plan/', ajax_redact_plan, name="ajax_redact_plan"),
    path('help/', help_page, name="help"),
]