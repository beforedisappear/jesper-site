from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

from .utils import user_directory_path, correct_email
from mptt.models import MPTTModel, TreeForeignKey
from uuslug import uuslug, slugify

class CustomAccountManager(BaseUserManager):
   def create_user(self, email, username, password=None, **other_fields):
      if not email:
         email = username + '@telegram.com'
         #raise ValueError(_('Please provide an email address'))
      user=self.model(username=username, email=correct_email(email), **other_fields)
      user.set_password(password)
      user.save()
      return user

   def create_superuser(self, email, username, password, **other_fields):
      other_fields.setdefault('is_staff',True)
      other_fields.setdefault('is_superuser',True)
      other_fields.setdefault('is_active',True)
      if other_fields.get('is_staff') is not True:
         raise ValueError(_('Please assign is_staff=True for superuser'))
      if other_fields.get('is_superuser') is not True:
         raise ValueError(_('Please assign is_superuser=True for superuser'))
      return self.create_user(email, username, password, **other_fields)

     
class MyUser(AbstractBaseUser, PermissionsMixin):
   email = models.EmailField(_('Email'), unique=True)
   username= models.CharField(_('UserName'), max_length=25, db_index=True)
   first_name = models.CharField(_('First Name'), max_length=25, blank=True)
   last_name = models.CharField(_('Last Name'), max_length=25, blank=True)
   is_staff = models.BooleanField(_('Is staff'), default=False)
   is_active = models.BooleanField(_('Is active'), default=True)
   
   id = models.AutoField(primary_key=True)
   userslug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='UserSlug')
   userpic = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name='Аватар', default='baseuserpic.jpg' )
   theme = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name='Фон')
   description = models.CharField(max_length=150, blank=True, verbose_name='Пару слов о себе')
   date_joined = models.DateTimeField(_("date joined"), blank=True, null=True, auto_now_add=True)
   email_verify = models.BooleanField(_('Verified email'), default=False)

   objects = CustomAccountManager()
   
   USERNAME_FIELD='email' #the name of the field on the user model that is used as the unique identifier
   REQUIRED_FIELDS=['username'] # запрашиваемое поле при вызове createsuperuser

   def __str__(self):
      return self.email
    
   def save(self, *args, **kwargs):
      if self.is_superuser:                                                               #slug for superuser                                      
         self.userslug = self.username.lower().replace(' ', '-')
      try:
         super(MyUser, self).save(*args, **kwargs)
      except:
         raise ValueError(_('This admin already exists!'))
      self.update_user_slug() 
      
   def update_user_slug(self):
      # You now have both access to self.id
      if not self.is_superuser: 
         #now have both access to self.id
         self.userslug = str(self.id) + '-' + slugify(self.username.lower().replace(' ', '-')) #slug for user
         MyUser.objects.filter(id=self.id).update(userslug=self.userslug)
         
   def get_absolute_url(self):
        return reverse('user-page', args=[self.userslug])
     
   class Meta:
      verbose_name = 'Пользователь'
      verbose_name_plural = 'Пользователи'
      
      
#хранение контента
class articles(models.Model):
   SECTIONS = [('economy', 'Экономика'), ('dev', 'Разработка | IT'), ('life', 'Жизнь')]
   section = models.CharField(max_length=15, choices=SECTIONS)
   title = models.CharField(max_length=150, verbose_name='Заголовок')
   slug = models.SlugField(max_length=1001, unique=True, db_index=True, verbose_name='URL')
   subtitle = models.CharField(max_length=350, verbose_name='Подзаголовок', blank=True)
   #many articles to one user
   author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Автор')
   text = models.TextField(blank=True, verbose_name='Текст')
   time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
   is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
   content = models.FileField(upload_to='files/%Y/%m/%d', blank=True, validators=[
      FileExtensionValidator(
         allowed_extensions=['jpg', 'png', 'mp4', 'gif', 'mov', 'heic'], 
         message='Некорректный формат файла!',
         )
      ])
   
   #формирование маршрута к конкретной записи
   def get_absolute_url(self):
      # 'article' - имя маршрута в urls.py
      return reverse("article", kwargs={"post_slug": self.slug,"section_slug": self.section})
   
   def __unicode__(self):
      return self.title

   #транслитерация слага
   def save(self, *args, **kwargs):
      self.slug = uuslug(self.title, instance=self)
      super(articles, self).save(*args, **kwargs) 
      
   #тип файла
   def get_file_type(self):
      a = self.content.name.find('.') + 1
      if self.content.name[a:] in ['jpg', 'png', 'heic']: return 'photo'
      elif self.content.name[a:] in  ['mp4', 'mov', 'heic']: return 'video'
   
   #метод для отображения объекта
   def __str__(self):
      return self.title
   
   #вложенный класс для настройки админ панели
   class Meta:
      verbose_name = 'Статьи'
      verbose_name_plural = 'Статьи'
      #сортировка отображения статей
      ordering = ['time_create']
   
   
class comments(MPTTModel):
   # через related_name обращаемся к множеству объектов класса comments, связанных с объектом класса articles
   post = models.ForeignKey(articles, on_delete=models.CASCADE, related_name='cmnts', verbose_name='Статья')
   author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, verbose_name='Автор комментария')
   text = models.TextField(verbose_name='Текст комментария')
   time_create = models.DateTimeField(auto_now_add=True)
   is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
   #many answers to one parent comment (tree, data structure)
   parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children', db_index=True, verbose_name='Род.Коммент')
   
   class Meta:
      verbose_name = 'Комментарии'
      verbose_name_plural = 'Комментарии'
      ordering = ['time_create']
      
   #метод для отображения объекта
   def __str__(self):
      return self.text
   
   
class likes(models.Model):
   #many likes to one article
   post = models.ForeignKey(articles, on_delete=models.CASCADE, related_name='likes', verbose_name='Статья')
   like = models.BooleanField(default=False, verbose_name='Лайки')
   liked_by = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, verbose_name='Автор лайка')
   time_create = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      verbose_name = 'Лайки'
      verbose_name_plural = 'Лайки'
      ordering = ['time_create']
      