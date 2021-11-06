from django.contrib import admin
from .models import *


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']


class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'template', 'date']


class FieldAdmin(admin.ModelAdmin):
    list_display = ['title', 'type_of_data', 'input_name']


class TypeField(admin.ModelAdmin):
    list_display = ['title']


class InputAdmin(admin.ModelAdmin):
    list_display = ['title', 'css_class']


admin.site.register(Template, TemplateAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Type, TypeField)
admin.site.register(Input, InputAdmin)
