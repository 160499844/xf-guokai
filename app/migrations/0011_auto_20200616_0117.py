# Generated by Django 2.0.1 on 2020-06-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_sysuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='timu',
            field=models.FileField(upload_to='', verbose_name='题目'),
        ),
    ]
