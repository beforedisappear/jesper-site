# Generated by Django 4.1.5 on 2023-01-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_myuser_email_verify_delete_сomment_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email_verify',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
    ]
