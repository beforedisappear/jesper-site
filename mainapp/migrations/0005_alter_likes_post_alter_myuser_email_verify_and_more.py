# Generated by Django 4.1.5 on 2023-01-28 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_myuser_email_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='mainapp.articles', verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email_verify',
            field=models.BooleanField(default=False, verbose_name='Verified email'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(db_index=True, max_length=25, verbose_name='UserName'),
        ),
    ]