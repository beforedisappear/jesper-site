from django.apps import AppConfig

#конфигурация нашего приложения
class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
