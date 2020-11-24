from django.shortcuts import render
import xlrd
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .application import *
import threading
from io import BytesIO
import xlwt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import decimal
# Create your views here.
@csrf_exempt
def import_excel(request):
    loginUser = request.session.get("loginUser", default=None)


    """导入excel表数据"""
    msg = {"msg":"OK"}
    if loginUser == None:
        msg = {"msg": "请登录"}
        return HttpResponse(json.dumps(msg), content_type="application/json")

    excel_file = request.FILES.get('excel_file', '')  # 获取前端上传的文件
    file_type = excel_file.name.split('.')[-1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:
        # 支持这两种文件格式

        # 开始运行
        settings = Settings.objects.filter(loginUser=loginUser).first()
        ts = settings.threads
        allUsers = 0
        data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
        tables = data.sheets()  # 得到excel中数据表sheets1，sheets2...
        # 循环获取每个数据表中的数据并写入数据库
        for table in tables:
            rows = table.nrows  # 总行数
            for row in range(1, rows):  # 从1开始是为了去掉表头
                row_values = table.row_values(row)  # 每一行的数据

                name = row_values[0]
                username = row_values[1]
                password = row_values[2]
                kecheng = row_values[3]

                #删除旧的用户数据
                us = UserData.objects.filter(username=username).filter(kecheng=kecheng)
                for u in us:
                    u.delete()
                ls = Logs.objects.filter(username=username).filter(kecheng=kecheng)
                for l in ls:
                    l.delete()

                userData = UserData()
                userData.username = str(username)
                userData.loginUser = loginUser
                userData.password = str(password).replace(".0","")
                userData.kecheng = str(kecheng)
                userData.name = str(name)
                userData.status = 'R'
                userData.save()
                print(row_values)

                allUsers += 1

                userPoolAddUser(str(username),str(name),str(userData.password),str(kecheng))

        if ts > allUsers:
            ts = allUsers
        for i in range(0,ts):
            t1 = threading.Thread(target=userPool, args=(loginUser,int(settings.period),int(settings.accuracy),))  # 调用Thread, 创建线程的对象，不会创建线程
            t1.start()
            time.sleep(10)

        return HttpResponse(json.dumps(msg), content_type="application/json")
    else:
        msg = {"msg": "格式错误!"}
        return HttpResponse(json.dumps(msg), content_type="application/json")

@csrf_exempt
def save(request):
    loginUser = request.session.get("loginUser", default=None)
    if loginUser == None:
        msg = {"msg": "请登录"}
        return HttpResponse(json.dumps(msg), content_type="application/json")

    ts = request.POST['ts']
    times = request.POST['times']
    accuracy = request.POST['accuracy']

    settings = Settings.objects.filter(loginUser=loginUser).first()
    if settings == None:
        settings = Settings()
    settings.threads = int(ts)
    settings.period = int(times)
    settings.loginUser = loginUser
    settings.accuracy = int(accuracy)
    settings.save()
    msg = {"msg": "保存成功!"}
    return HttpResponse(json.dumps(msg), content_type="application/json")

@csrf_exempt
def login(request):
    message = {'msg': ''}
    if request.method == 'POST':  # 当提交表单
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = SysUser.objects.get(username=username)
            _password = user.password
            if _password == password:
                message = {'msg': '登录成功'}
                request.session['loginUser'] = user.username
            else:
                message = {'msg': '帐号或密码错误'}
        except:
            message = {'msg': '帐号不存在'}

    return HttpResponse(json.dumps(message), content_type="application/json")

#退出登陆
def exit(request):
    try:
        del request.session["loginUser"]
    except KeyError:
        pass
    return render(request, 'adminLogin.html')
def index(request):
    settings = Settings.objects.all().first()
    return render(request, 'index.html', {"settings":settings})

def toLogin(request):
    return render(request, 'adminLogin.html', {})
@csrf_exempt
def list(request):
    loginUser = request.session.get("loginUser", default=None)
    if loginUser == None:
        return render(request, 'adminLogin.html', {})

    if request.method == 'POST':  # 当提交表单
        startTime = request.POST['startTime']
        endTime = request.POST['endTime']
        startTime = str(startTime).replace("T"," ") + ":00"
        endTime = str(endTime).replace("T"," ")+ ":00"
        print("%s --> %s" %(startTime,endTime))
        contact_list = Logs.objects.filter(loginUser=loginUser).filter(create_dt__gte=startTime).filter(create_dt__lte=endTime).order_by('-id')
    else:

        contact_list = Logs.objects.filter(loginUser=loginUser).order_by('-id')
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'contacts': contacts})

def getLogs(request):
    loginUser = request.session.get("loginUser", default=None)
    if loginUser == None:
        msg = {"msg": "请登录"}
        return HttpResponse(json.dumps(msg), content_type="application/json")
    list = Logs.objects.filter(loginUser=loginUser).order_by('-create_dt')[:20]
    result = []
    for item in list:
        dict = {
            "name" : item.name,
            "kecheng" : item.kecheng,
            "timu" : item.timu,
            "score" : item.score,
            "create_dt" :item.create_dt,
            "status" :item.status,
        }
        #print(dict)
        result.append(dict)
    msg = {"msg": result}
    return HttpResponse(json.dumps(msg), content_type="application/json")

def download(request):
    loginUser = request.session.get("loginUser", default=None)
    if loginUser == None:
        msg = {"msg": "请登录"}
        return HttpResponse(json.dumps(msg), content_type="application/json")
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
    sheet.write(0, 0, '姓名', style_heading)
    sheet.write(0, 1, '用户名', style_heading)
    sheet.write(0, 2, '密码', style_heading)
    sheet.write(0, 3, '课程', style_heading)
    sheet.write(0, 4, '题目', style_heading)
    sheet.write(0, 5, '分数', style_heading)

    # 写入数据
    data_row = 1
    list = UserData.objects.filter(loginUser=loginUser)
    map = {}
    for item in list:
        map[item.username] = item.password
    # User.objects.all()#这个是查询条件,可以根据自己的实际需求做调整.
    for i in Logs.objects.filter(status='C').filter(loginUser=loginUser):
        password = map[i.username]


        # 格式化datetime
        sheet.write(data_row, 0, str(i.name))
        sheet.write(data_row, 1, str(i.username))
        sheet.write(data_row, 2, str(password))
        sheet.write(data_row, 3, str(i.kecheng))
        sheet.write(data_row, 4, str(i.timu))
        sheet.write(data_row, 5, str(i.score))

        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response