# Generated by Django 2.2.1 on 2020-06-19 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20200618_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='accuracy',
            field=models.IntegerField(default=100, null=True, verbose_name='正确率'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='period',
            field=models.IntegerField(default=3, verbose_name='延迟间隔'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='threads',
            field=models.IntegerField(default=1, null=True, verbose_name='线程数'),
        ),
    ]
