# Generated by Django 2.0.1 on 2020-06-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200616_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysuser',
            name='name',
            field=models.CharField(max_length=56, null=True, verbose_name='姓名'),
        ),
    ]