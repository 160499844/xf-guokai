# Generated by Django 2.0.1 on 2020-06-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userdata_kecheng'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='threads',
            field=models.IntegerField(null=True, verbose_name='线程数'),
        ),
    ]
