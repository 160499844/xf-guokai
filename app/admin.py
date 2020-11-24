from django.contrib import admin
from .models import *
from django.http import HttpResponse
from io import BytesIO
import xlwt
# Register your models here.
# 导出excel数据
def export_to_csv(modeladmin, request, queryset):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入文件标题
    sheet.write(0,0,'用户名',style_heading)
    sheet.write(0,1,'课程',style_heading)
    sheet.write(0,2,'题目',style_heading)
    sheet.write(0,3,'分数',style_heading)

    # 写入数据
    data_row = 1
    #User.objects.all()#这个是查询条件,可以根据自己的实际需求做调整.
    for i in Logs.objects.filter(status='T'):
        # 格式化datetime
        sheet.write(data_row,0,str(i.name))
        sheet.write(data_row,1,str(i.kecheng))
        sheet.write(data_row,2,str(i.timu))
        sheet.write(data_row,3,str(i.score))

        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response
export_to_csv.short_description = '导出ESV'



class SysUserAdmin(admin.ModelAdmin):
    list_display = ('username','password','name')
    #exclude = ('password',)
admin.site.register(SysUser,SysUserAdmin)

class PorjectAdmin(admin.ModelAdmin):
    list_display = ('loginUser','username','name','kecheng','timu','score','status','create_dt')
    list_filter = ('status',)
    actions = [export_to_csv]

admin.site.register(Logs,PorjectAdmin)


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('loginUser','name','username','password','kecheng','status','create_dt')
admin.site.register(UserData,UserDataAdmin)

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('period','threads','accuracy')
admin.site.register(Settings,SettingsAdmin)