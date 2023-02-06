from django.urls import path, include
from django.conf.urls import *

from .views import *

#name - имя страницы (неявный url адрес)
#as_view() - вызов ф. связи класса с маршрутом
#social-auth/ url шаблон для авторизации через социальные сети
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('economy/', economy.as_view(), name='economy'),
    path('dev/', dev.as_view(), name='dev'),
    path('life/', life.as_view(), name='life'),
    path('logout/', logout_user, name='logout'),
    path('<slug:section_slug>/article/<slug:post_slug>/', ShowArticle.as_view(), name='article'),
    path('page/<slug:username>/', userpage.as_view(), name='user-page'),
    path('page/<slug:username>/settings', userpagesettings.as_view(), name='user-page-set'),
    path('account/active/<uidb64>/<token>/', EmailVerify.as_view(), name='userverify'),
    path('account/reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='userpasswordreset'),
    path('social-auth/', include('social_django.urls', namespace='social')),
 ]
