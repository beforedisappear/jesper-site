from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
   list_display = ('username', 'email', 'is_active', 'is_staff', 'email_verify', 'date_joined', 'is_superuser',)
   #добавляем отображение кастомных полей в админке
   fieldsets = (
    (None, {'fields': ('email','username', 'password')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    (_('Permissions'), {
        'fields': ('email_verify', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    (_('Additional Info'), {'fields': ('userpic', 'theme', 'description', 'userslug')}),
   )
   readonly_fields = ["date_joined", "is_superuser"]

admin.site.register(MyUser, UserAdmin)

class articlesAdmin(admin.ModelAdmin):
   # отображаемые поля
   list_display = ('id', 'section', 'title', 'subtitle', 'author', 'time_create', 'content', 'is_published')
   # кликабельность поля
   list_display_links = ('id', 'title')
   # по каким поляем работает поиск
   search_fields = ['section', 'title', 'subtitle', 'text', 'author'] 

admin.site.register(articles, articlesAdmin)

class commentsAdmin(admin.ModelAdmin):
   model = comments
   list_display = ('post', 'author', 'parent', 'text', 'time_create', 'is_active',)
   list_display_links = ('post', 'author', 'parent',)
   search_fields = ['post', 'author', 'text', ]

admin.site.register(comments, commentsAdmin)

# class commentsanswerAdmin(admin.ModelAdmin):
#    model = сomment_answer
#    list_display = ('comment', 'author', 'text', 'time_create', 'is_active')
#    list_display_links = ('comment', 'author')
#    search_fields = ['comment', 'author', 'text']

# admin.site.register(сomment_answer, commentsanswerAdmin)

class likesAdmin(admin.ModelAdmin):
   model = likes
   list_display = ('post', 'liked_by', 'time_create')
   
admin.site.register(likes, likesAdmin)
