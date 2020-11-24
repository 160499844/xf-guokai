from django.db import models
import django.utils.timezone as timezone
# Create your models here.
#
class SysUser(models.Model):
    username = models.CharField(u'用户名', max_length=56)
    name = models.CharField(u'姓名', max_length=56,null=True)
    password = models.CharField(u'密码', max_length=56)


    def __unicode__(self):
       return self.name
    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'


class UserData(models.Model):
    GENDER_CHOICES = (
        (u'S', u'完成'),
        (u'D', u'待处理'),
        (u'F', u'取消'),
    )

    FEE_CHOICES = (
        (u'D', u'未开始'),
        (u'R', u'运行中'),
        (u'W', u'完成'),
        (u'S', u'失败'),
    )
    loginUser = models.CharField(u'导入用户', max_length=50, null=True)
    username = models.CharField(u'用户名',max_length=50)
    name = models.CharField(u'姓名',max_length=50,null=True)
    password = models.CharField(u'密码',max_length=50)
    kecheng = models.CharField(u'课程',max_length=50,null=True)
    #accuracy = models.DecimalField(u'正确率',null=True,max_digits=2, decimal_places=1)

    status = models.CharField(u'状态', choices=FEE_CHOICES, max_length=10, blank=True, default='D')

    type = models.CharField(u'进度', choices=GENDER_CHOICES, max_length=10, null=True,blank=True,default='D')

    create_dt = models.DateTimeField(u'创建时间', default=timezone.now, blank=True)




    def __unicode__(self):
        return self.loginUser

    class Meta:
        verbose_name = '用户记录'
        verbose_name_plural = verbose_name

class Settings(models.Model):
    loginUser = models.CharField(u'用户', max_length=50, null=True)
    period = models.IntegerField(u'延迟间隔',default=3)
    threads = models.IntegerField(u'线程数',null=True,default=1)
    accuracy = models.IntegerField(u'正确率', null=True,default=100)

    def __unicode__(self):
        return self.period

    class Meta:
        verbose_name = '延迟间隔设置'
        verbose_name_plural = verbose_name

class Logs(models.Model):
    FEE_CHOICES = (
        (u'T', u'测试'),
        (u'S', u'视频'),
        (u'J', u'记录'),
        (u'C', u'成绩'),

    )

    username = models.CharField(u'用户名', max_length=50,null=True)
    loginUser = models.CharField(u'操作用户', max_length=50,null=True)
    name = models.CharField(u'姓名', max_length=50)
    kecheng = models.CharField(u'课程', max_length=50)
    timu = models.CharField(u'题目', max_length=100)
    score = models.CharField(u'分数',null=True,max_length=10)
    create_dt = models.CharField(u'创建时间', blank=True,null=True,max_length=50)
    status = models.CharField(u'类型', choices=FEE_CHOICES, max_length=10, blank=True)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = verbose_name

class Timu_Answer(models.Model):
    kecheng = models.CharField(u'课程id', max_length=255,null=True)
    title = models.CharField(u'题目', max_length=255)
    answer = models.CharField(u'答案', max_length=255)


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = '答案记录'
        verbose_name_plural = verbose_name


