# Generated by Django 4.1.5 on 2023-01-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_comments_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='email_verify',
            field=models.BooleanField(default=True, verbose_name='Verified'),
        ),
        migrations.DeleteModel(
            name='сomment_answer',
        ),
    ]
