# Generated by Django 2.2.1 on 2020-06-21 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20200620_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='timu_answer',
            name='kecheng',
            field=models.CharField(max_length=255, null=True, verbose_name='课程'),
        ),
    ]