# Generated by Django 2.2.1 on 2020-06-17 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_logs_loginuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='loginUser',
            field=models.CharField(max_length=50, null=True, verbose_name='用户'),
        ),
    ]
