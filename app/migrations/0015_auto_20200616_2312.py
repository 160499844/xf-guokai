# Generated by Django 2.2.1 on 2020-06-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_logs_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='kecheng',
            field=models.CharField(max_length=50, verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='name',
            field=models.CharField(max_length=50, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='score',
            field=models.CharField(max_length=10, null=True, verbose_name='分数'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='timu',
            field=models.CharField(max_length=100, verbose_name='题目'),
        ),
        migrations.AlterField(
            model_name='timu_answer',
            name='answer',
            field=models.CharField(max_length=255, verbose_name='答案'),
        ),
        migrations.AlterField(
            model_name='timu_answer',
            name='title',
            field=models.CharField(max_length=255, verbose_name='题目'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='kecheng',
            field=models.CharField(max_length=50, null=True, verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='password',
            field=models.CharField(max_length=50, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='username',
            field=models.CharField(max_length=50, verbose_name='用户名'),
        ),
    ]
