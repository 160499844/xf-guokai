from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import pickle
import json
from urllib import parse
import urllib3
urllib3.disable_warnings()
import math
import queue
import datetime
from .models import *


q = queue.Queue()
import os
#geckodriver_path = r'D:\resource\geckodriver.exe'
geckodriver_path = 'C:\\Users\\Administrator\\Desktop\\国开自动刷课系统\\国开自动刷课系统\\geckodriver.exe'




#session = requests.session()
#access_token = ""
timuMaps = {}
SleepTime = 3
accuracy = 100
dir_path = "C:\\Users\\Administrator\\Desktop\\国开自动刷课系统\\国开自动刷课系统\\临时文件\\"

userInfoMap = {}

def saveUserInfo(username,user_read_movies,user_kecheng):
    """保存用户阅读记录
    #已观看的视频地址保存
    """

    f1 = open(dir_path + username + '_' + user_kecheng + '.txt', 'a+')
    f1.writelines(user_read_movies+'\n')
    f1.close()
def checkReadList(username,link,user_kecheng):

    f1 = open(dir_path + username + '_' + user_kecheng +'.txt', 'r')
    list = f1.readlines()
    f1.close()
    if link + '\n' in list:
        return True

    return False


def login(driver,username,password,user_kecheng):
    """登录"""
    driver.get("http://passport.ouchn.cn/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dstudentspace%26redirect_uri%3Dhttp%253A%252F%252Fstudent.ouchn.cn%252F%2523%252Fsignin-oidc%2523%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520ouchnuser%2520ouchnstudentspaceapi%26state%3D0bbb13ff0f9b4e14b40be529069945c1%26nonce%3D4b2f327eb1ca428d8552049c11b8d97e")
    usernameDiv = driver.find_element_by_xpath('//*[@id="username"]')
    passwordDiv = driver.find_element_by_xpath('//*[@id="password"]')
    usernameDiv.send_keys(str(username))
    passwordDiv.send_keys(str(password))
    submit = driver.find_element_by_xpath('/html/body/div/div/div/form/div/div/div[4]/button')
    time.sleep(1)
    submit.click()
    cookies = driver.get_cookies()

    f = open(dir_path + 'cookies.pkl', 'wb')
    f.write(pickle.dumps(cookies))
    f.close()

    saveUserInfo(username,'',user_kecheng)

def  getCourseInfo(access_token,kecheng):
    """获取我的全部课程"""
    session = requests.session()
    session.verify = False
    session.get('http://student.ouchn.cn/#/home')

    headers = {
        'Referer': 'http://student.ouchn.cn/',
        'Origin': 'http://student.ouchn.cn',
        'Authorization': 'Bearer '+ access_token
    }
    list = []

    getCourseInfoUrl = 'http://117.78.41.66:9005/api/MyCourse/CoursesSemestersInfo'
    js = session.get(getCourseInfoUrl,headers=headers).json()
    print(js['Data']['LearningCourses'])
    dict = {}
    print("我的课程列表")
    for course in js['Data']['LearningCourses']:
        #http://117.78.41.66:9005/api/MyCourse/GetEnterCourseUrl?Site=http://shanxi3.ouchn.cn&CourseCode=04391&Signature=8cf5a61eb5eabb6f26c1ec57dba4176224d9208f&nowtime=1591967683635
        courseUrl = "http://117.78.41.66:9005/api/MyCourse/GetEnterCourseUrl?Site="+course['Url']+"&CourseCode="+course['CourseCode']+"&Signature=" + course['Signature']

        print("%s %s" % (course['CourseName'], courseUrl))
        if kecheng == course['CourseName']:
        # if '习近平新时代中国特色社会主义思想' == course['CourseName'] \
        #         or '毛泽东思想和中国特色社会主义理论体系概论' == course['CourseName'] \
        #         or '思想道德修养与法律基础' == course['CourseName']:

            list.append(courseUrl)

    #打开课程

    course_list = []
    for link in list:
        t = time.time()
        t = int(round(t * 10000))
        courseUrl = link + "&nowtime=" + str(t)
        obj = session.get(courseUrl, headers=headers).json()
        print(obj)
        course_link = obj['Data']
        course_list.append(course_link)


    return course_list

def getUserInfo(access_token):
    headers = {
        'Referer': 'http://student.ouchn.cn/',
        'Origin': 'http://student.ouchn.cn',
        'Authorization': 'Bearer ' + access_token
    }
    url = "http://passport.ouchn.cn/connect/userinfo"
    session = requests.session()
    js = session.get(url,headers=headers).json()
    print(js)

def sendTiMuAnswer(content,kecheng):
    """获取题目答案"""

   # tis = Timu_Answer.objects.filter(kecheng=kecheng)


    Soup = BeautifulSoup(content, "lxml")
    title = Soup.title
    list = []  # 答案保存
    print("获取题目答案")
    divs1 = Soup.find_all("div", class_="que truefalse deferredfeedback notyetanswered")
    for div in divs1:
        timu = div.find("div", class_="qtext").find("p").get_text().replace("（ \xa0\xa0）。", "").replace("（","").replace("）","").lstrip()
        print(timu)
        answerDivs = div.find("div", class_="answer")
        for item in answerDivs:
            """遍历答案"""
            if item == '\n':
                continue
            inputId = item.find("input").get("id")
            txt = item.find("label").get_text()

            timuEntity = Timu_Answer.objects.filter(title__contains=timu)
            if timuEntity.count() != 0 and timuEntity.first().answer in txt:
                list.append(inputId)
            # if timu in timuMaps.keys() and timuMaps[timu] in txt:
            #     list.append(inputId)

    divs2 = Soup.find_all("div", class_="que multichoice deferredfeedback notyetanswered")
    for div in divs2:
        timu = div.find("div", class_="qtext").find("p").get_text().replace("（ \xa0\xa0）。", "").replace("（","").replace("）","").lstrip()
        print(timu)
        answerDivs = div.find("div", class_="answer")

        for item in answerDivs:

            """遍历答案"""
            if item == '\n':
                continue
            inputId = item.find("input").get("id")
            txt = item.find("label").get_text()
            timuEntity = Timu_Answer.objects.filter(title__contains=timu)
            if timuEntity.count() != 0 and timuEntity.first().answer in txt:
                list.append(inputId)
            # if timu in timuMaps.keys() and timuMaps[timu] in txt:
            #     list.append(inputId)

    return list
def getTiMuAnswer(content,kecheng):
    """获取题目答案"""
    Soup = BeautifulSoup(content, "lxml")
    title = Soup.title

    print("获取题目答案")

    # 获取正确的判断题
    divs1 = Soup.find_all("div", class_="que truefalse deferredfeedback notanswered")
    for div in divs1:
        timu = div.find("div", class_="qtext").find("p").get_text()

        answerDivs = div.find("div", class_="rightanswer").get_text()
        answerDivs = str(answerDivs).replace("正确的答案是“", "").replace("”。", "")

        #timuMaps[str(timu).replace("（ \xa0\xa0）。", "")] = answerDivs
        timu = str(timu).replace("（ \xa0\xa0）。", "").replace("（","").replace("）","").lstrip()
        print(timu)
        print(answerDivs)
        entity = Timu_Answer()
        entity.kecheng = kecheng
        entity.title = timu
        entity.answer = answerDivs
        entity.save()
        # entity = Timu_Answer.objects.filter(kecheng=kecheng).filter(title__contains=timu)
        # if entity.count() == 0:
        #     entity = Timu_Answer()
        #     entity.kecheng = kecheng
        #     entity.title = timu
        #     entity.answer = answerDivs
        #     entity.save()

    # 获取正确的单选
    divs2 = Soup.find_all("div", class_="que multichoice deferredfeedback notanswered")
    for div in divs2:
        timu = div.find("div", class_="qtext").find("p").get_text()
        answerDivs = div.find("div", class_="rightanswer").get_text()
        answerDivs = str(answerDivs).replace("正确答案是：", "")

        #timuMaps[str(timu).replace("（ \xa0\xa0）。", "")] = answerDivs

        timu = str(timu).replace("（ \xa0\xa0）。", "").replace("（","").replace("）","").lstrip()
        print(timu)
        print(answerDivs)
        #entity = Timu_Answer.objects.filter(title__contains=timu)
        #if entity.count() == 0:
        entity = Timu_Answer()
        entity.kecheng = kecheng
        entity.title = str(timu).replace("（ \xa0\xa0）。", "")
        entity.answer = answerDivs
        entity.save()

def getkechenLinks(content):
    """获取课程视频"""
    list = []
    Soup = BeautifulSoup(content, "lxml")
    ul = Soup.find("ul",class_="flexsections flexsections-level-1")
    all_links = ul.find_all("a")
    for item in all_links:
        url = item.get('href')
        if 'url/view.php?id=' in url:
            print(url)
            list.append(url)
    new_li = []
    for i in list:
        if i not in new_li:
            new_li.append(i)
    return new_li

def getCeyanLinks(content):
    """获取测验链接"""
    list = []
    Soup = BeautifulSoup(content, "lxml")
    ul = Soup.find("ul",class_="flexsections flexsections-level-1")
    all_links = ul.find_all("a")
    for item in all_links:
        url = item.get('href')
        #span = item.find("span").get_text()

        if 'quiz/view.php?id=' in url:
            print(url)
            list.append(url)
    new_li = []
    for i in list:
        if i not in new_li:
            new_li.append(i)
    return new_li
def getMoviesSubmitAdress(curUrl):
    url = ""
    print("获取当前视频url地址 %s" % curUrl)
    if '&sectionid' in curUrl:
        # 组装视频url
        #http://shanxi3.ouchn.cn/theme/blueonionre/modulesCompletion.php?cmid=546123&id=4187&sectionid=100637
        #http://xian.ouchn.cn/theme/blueonionre/modulesCompletion.php?cmid=546036&id=4610&sectionid=104886
        indexUrl = str(curUrl).split("/course")[0]
        params = parse.parse_qs(parse.urlparse(curUrl).query)
        cmid = params['mid'][0]
        id = params['id'][0]
        sectionid = params['sectionid'][0]
        url = indexUrl + "/theme/blueonionre/modulesCompletion.php?cmid=%s&id=%s&sectionid=%s" %(cmid,id,sectionid)
    return url
def playMp4(driver):
    """播放视频"""


    curUrl = driver.current_url
    address = getMoviesSubmitAdress(curUrl)
    if "" != address:
        return address
        # try:
        #     """如果匹配到视频，自动播放视频"""
        #     video = driver.find_element_by_tag_name("video")
        #     canvas = driver.find_element_by_tag_name("canvas")
        #     if video == None:
        #         return
        #     url = driver.execute_script("return arguments[0].currentSrc;", video)
        #     #print("提交观看请求:%s" % address)
        #     #print("捕获到视频地址:%s" % url)
        #
        #     return address
        #
        # except Exception as e:
        #     print(e)
    return ""
def playTest(driver,username,name,loginUser,zhuanti_count,kecheng):
    """答题"""
    button = driver.find_element_by_css_selector("button[class='btn btn-secondary']")
    text = button.text  # 获取元素文本信息
    print(text)  # 打印元素文本
    getAns = False

    hasAnswer = True
    #判断是否有答案
    print("课程id:%s" %kecheng)
    ks = Timu_Answer.objects.filter(kecheng=kecheng)
    if ks.count() == 0:
        hasAnswer = False

    if hasAnswer:
        #有答案
        if '现在参加测验' == text or '继续上次答题' == text or '再次尝试此测验' == text:
            time.sleep(SleepTime)
            button.click()
            answers = sendTiMuAnswer(driver.page_source, kecheng)
            print("搜索到答案")
            print(",".join(answers))

            submitEnd = False

            if answers:
                for answer in answers:
                    # time.sleep(SleepTime)
                    driver.find_element_by_id(answer).click()
                # 判断是否有下一页
                while submitEnd == False:
                    nextButton = driver.find_element_by_name('next')
                    if nextButton:
                        time.sleep(SleepTime)
                        nextButton.click()

                        answers = sendTiMuAnswer(driver.page_source, kecheng)
                        print("搜索到答案")
                        print(",".join(answers))
                        if answers:
                            # 使用正确率x/y=(accuracy/100)
                            answers = accuracyUtils(answers)
                            for answer in answers:
                                if answer == None:
                                    continue
                                driver.find_element_by_id(answer).click()
                    # 结束答题
                    submits = driver.find_elements_by_css_selector("button[class='btn btn-secondary']")
                    for submit in submits:
                        text = submit.text  # 获取元素文本信息
                        print(text)  # 打印元素文本
                        if '提交所有答案并结束' == text:
                            time.sleep(SleepTime)
                            submit.click()
                            # 弹出窗口
                            confirm = driver.find_element_by_css_selector("input[class='btn btn-primary m-r-1']")
                            confirm.click()
                            print("答题完毕！")
                            submitEnd = True
                            time.sleep(SleepTime)
                            driver.find_element_by_link_text("结束回顾").click()
                            break
            print("获取当前页面分数")
            # print(driver.page_source,driver.title)
            #getSorce(driver.page_source, driver.title, username, name, loginUser, zhuanti_count)
    else:
        #无答案

        if '现在参加测验' == text or '继续上次答题' == text:
            time.sleep(SleepTime)
            button.click()
            nextButton = driver.find_element_by_name('next')
            text = nextButton.text  # 获取元素文本信息
            print(text)  # 打印元素文本
            over = False
            while over==False:
                nextButton = driver.find_element_by_name('next')
                time.sleep(SleepTime)
                nextButton.click()

                #结束答题
                submits = driver.find_elements_by_css_selector("button[class='btn btn-secondary']")
                for submit in submits:
                    text = submit.text  # 获取元素文本信息
                    print(text)  # 打印元素文本
                    if '提交所有答案并结束' == text:
                        time.sleep(SleepTime)
                        submit.click()
                        # 弹出窗口
                        confirm = driver.find_element_by_css_selector("input[class='btn btn-primary m-r-1']")
                        confirm.click()
                        over = True
                        print("答题完毕！")
                        getTiMuAnswer(driver.page_source,kecheng)
                        time.sleep(SleepTime)
                        driver.find_element_by_link_text("结束回顾").click()
                        getAns = True
                        break
        if '再次尝试此测验' == text:
            time.sleep(SleepTime)
            button.click()
            nextButton = driver.find_element_by_name('next')
            text = nextButton.text  # 获取元素文本信息
            print(text)  # 打印元素文本
            over = False
            while over == False:
                nextButton = driver.find_element_by_name('next')
                time.sleep(SleepTime)
                nextButton.click()

                # 结束答题
                submits = driver.find_elements_by_css_selector("button[class='btn btn-secondary']")

                for submit in submits:
                    text = submit.text  # 获取元素文本信息
                    print(text)  # 打印元素文本
                    if '提交所有答案并结束' == text:
                        time.sleep(SleepTime)
                        submit.click()
                        # 弹出窗口
                        confirm = driver.find_element_by_css_selector("input[class='btn btn-primary m-r-1']")
                        confirm.click()
                        over = True
                        print("答题完毕！")
                        time.sleep(SleepTime)
                        driver.find_element_by_link_text("结束回顾").click()
                        break

        # 获取答案
        huiguLink = driver.find_element_by_link_text("回顾")
        if huiguLink and getAns==False:
            time.sleep(SleepTime)
            huiguLink.click()
            getTiMuAnswer(driver.page_source,kecheng)
            time.sleep(SleepTime)
            driver.back()
        button = driver.find_element_by_css_selector("button[class='btn btn-secondary']")
        text = button.text  # 获取元素文本信息
        if '再次尝试此测验' == text:
            time.sleep(SleepTime)
            button.click()
            answers = sendTiMuAnswer(driver.page_source,kecheng)
            print("搜索到答案")
            print(",".join(answers))

            submitEnd = False

            if answers:
                for answer in answers:
                    #time.sleep(SleepTime)
                    driver.find_element_by_id(answer).click()
                # 判断是否有下一页
                while submitEnd == False:
                    nextButton = driver.find_element_by_name('next')
                    if nextButton:
                        time.sleep(SleepTime)
                        nextButton.click()

                        answers = sendTiMuAnswer(driver.page_source,kecheng)
                        print("搜索到答案")
                        print(",".join(answers))
                        if answers:
                            #使用正确率x/y=(accuracy/100)
                            answers = accuracyUtils(answers)
                            for answer in answers:
                                if answer == None:
                                    continue
                                driver.find_element_by_id(answer).click()
                    # 结束答题
                    submits = driver.find_elements_by_css_selector("button[class='btn btn-secondary']")
                    for submit in submits:
                        text = submit.text  # 获取元素文本信息
                        print(text)  # 打印元素文本
                        if '提交所有答案并结束' == text:
                            time.sleep(SleepTime)
                            submit.click()
                            # 弹出窗口
                            confirm = driver.find_element_by_css_selector("input[class='btn btn-primary m-r-1']")
                            confirm.click()
                            print("答题完毕！")
                            submitEnd = True
                            time.sleep(SleepTime)
                            driver.find_element_by_link_text("结束回顾").click()
                            break
            print("获取当前页面分数")
            #print(driver.page_source,driver.title)
            #getSorce(driver.page_source,driver.title,username,name,loginUser,zhuanti_count)
def getSorce(content,title,username,name,loginUser,zhuanti_count):
    #generaltable quizattemptsummary
    Soup = BeautifulSoup(content, "lxml")
    table = Soup.find("table", class_="generaltable quizattemptsummary")
    list = []
    trs = table.find_all("tr")
    if len(trs) > 0 :
        tr = trs[-1]
        tds = tr.find_all("td")
        if len(tds) > 2:
            sc = tds[2].get_text()
            logs = Logs()
            logs.kecheng = userInfoMap[username]
            logs.name = name
            logs.username = username
            logs.score = sc
            logs.loginUser = loginUser
            logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logs.timu = '专题' + str(zhuanti_count) + ' ' + title
            logs.status = 'T'
            logs.save()

def start(driver,username,name,user_kecheng,loginUser):
    """"访问课程"""
    index_url = ""
    driver.get(
        'http://passport.ouchn.cn/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dstudentspace%26redirect_uri%3Dhttp%253A%252F%252Fstudent.ouchn.cn%252F%2523%252Fsignin-oidc%2523%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520ouchnuser%2520ouchnstudentspaceapi%26state%3De24d2c9e1cec4ad487b72bb791f00de8%26nonce%3D94cbe2e6d2db4b809f7a2fe0d7664aed')
    f = open(dir_path + 'cookies.pkl', 'rb')
    cookies = pickle.load(f)
    f.close()

    # f1 = open(dir_path + 'userInfo.pkl', 'rb')
    # user_read_movies = pickle.load(f1)
    # print(user_read_movies)
    # f1.close()

    for cookie in cookies:
        if 'expiry' in cookies:
            del cookies['expiry']
    if 'domain' in cookies:
        del cookies['domain']
    for i in cookies:
        driver.add_cookie(i)
    driver.get('http://student.ouchn.cn/#/home')
    time.sleep(SleepTime)
    sessionId = driver.execute_script(
        'return sessionStorage.getItem("oidc.user:http://passport.ouchn.cn/:studentspace");')
    print("sessionId=%s" % sessionId)
    if sessionId != None:

        sessionObj = json.loads(sessionId)
        access_token = sessionObj['access_token']
        print("access_token=%s" % access_token)
        getUserInfo(access_token)

        course_list = getCourseInfo(access_token,user_kecheng)

        global userInfoMap
        userInfoMap[username] = user_kecheng

        for i in course_list:
            #先看完全部视频
            videoReadEnd = False
            ceyanEnd = False
            driver.get(i)
            if index_url == "":
                index_url = driver.current_url
            while videoReadEnd == False:
                driver.refresh()
                content = driver.page_source

                kechengs = getkechenLinks(content)
                count = 0

                # if videoReadEnd:
                #     break
                for kecheng in kechengs:
                    if count == len(kechengs)-1:
                        videoReadEnd = True
                        break
                    if checkReadList(username,kecheng,user_kecheng) == False:
                        count = 0
                    else:
                        count += 1
                        continue
                    print(kecheng)


                    try:
                        driver.get(kecheng)
                        title = driver.title
                        time.sleep(SleepTime)
                        adress = playMp4(driver)
                        if "" != adress:
                            driver.get(adress)
                            logs = Logs()
                            logs.kecheng = userInfoMap[username]
                            logs.name = name
                            logs.username = username
                            logs.timu = title
                            logs.status = 'S'
                            logs.loginUser = loginUser
                            logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            logs.save()

                            time.sleep(SleepTime)
                            driver.back()


                        time.sleep(SleepTime)
                        driver.back()

                        # 记录url
                        saveUserInfo(username, kecheng, user_kecheng)
                        break
                    except Exception as e:
                        print(e)

                        logs = Logs()
                        logs.kecheng = userInfoMap[username]
                        logs.name = name
                        logs.username = username
                        logs.timu = '视频播放失败'
                        logs.status = 'F'
                        logs.loginUser = loginUser
                        logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        logs.save()
                        time.sleep(30)
                        driver.back()
            #专题测验
            zhuanti_count = 0
            while ceyanEnd == False:
                driver.refresh()
                content = driver.page_source
                url = driver.current_url
                kechengs = getCeyanLinks(content)
                count = 0
                # if videoReadEnd:
                #     break
                if len(kechengs) ==0:
                    break
                for kecheng in kechengs:

                    if count == len(kechengs) - 1:
                        ceyanEnd = True

                    if checkReadList(username,kecheng,user_kecheng) == False:
                        count = 0
                    else:
                        count += 1
                        continue
                    print(kecheng)

                    try:
                        driver.get(kecheng)
                        time.sleep(SleepTime)
                        zhuanti_count += 1
                        id = str(kecheng).split("id=")[-1]
                        playTest(driver,username,name,loginUser,zhuanti_count,id)
                        # 记录url
                        saveUserInfo(username, kecheng, user_kecheng)
                        driver.get(url)
                        break
                    except Exception as e:
                        print(e)
                        logs = Logs()
                        logs.kecheng = userInfoMap[username]
                        logs.name = name
                        logs.username = username
                        logs.timu = '测验失败'
                        logs.status = 'F'
                        logs.loginUser = loginUser
                        logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        logs.save()
                        time.sleep(30)
                        driver.get(url)




    else:
        print('登录失败!')
        logs = Logs()
        logs.kecheng = '登录失败！'
        logs.name = name
        logs.loginUser = loginUser
        logs.username = username
        logs.timu = '登录失败！'
        logs.status = 'J'
        logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logs.save()
    return index_url

def userCreate(loginUser,username,name,password,user_kecheng):
    """创建用户浏览器"""

    print("当前登录用户:%s %s %s" %(username,password,user_kecheng))

    driver = webdriver.Firefox(executable_path=geckodriver_path)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)  # 这两种设置都进行才有效
    try:
        login(driver, username, password,user_kecheng)
        index_url = start(driver, username,name,user_kecheng,loginUser)
        logs = Logs()
        logs.kecheng = user_kecheng
        logs.name = name
        logs.loginUser = loginUser
        logs.username = username
        logs.timu = '该课程全部题目完成！'
        logs.status = 'J'
        logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logs.save()

        userData = UserData.objects.filter(username=username).first()
        userData.status = 'S'
        userData.save()
        print("%s 用户课程完毕，即将退出!" %loginUser)

        #保存成绩

        if index_url != None and index_url != "":
            print("index_url:%s" %index_url)
            index_url = index_url.split("course")[0]
            print("index_url:%s" % index_url)
            index_url =  index_url + 'grade/report/overview/index.php'
            print("index_url:%s" % index_url)
            driver.get(index_url)
            content = driver.page_source
            getGrade(content,loginUser,username,name,user_kecheng)

        time.sleep(10)
        driver.quit()
    except Exception as e:
        print(e)
        userData = UserData.objects.filter(username=username).first()
        userData.status = 'F'
        userData.save()
        print("错误")
def getGrade(content,loginUser,username,name,user_kecheng):
    """"保存成绩"""
    Soup = BeautifulSoup(content, "lxml")
    table = Soup.find("table", id="overview-grade").find("tbody")
    trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        title = tds[0].get_text()
        score = tds[1].get_text()
        if title == None or len(title) == 0 :
            continue
        if user_kecheng != title:
            continue
        logs = Logs()
        logs.kecheng = title
        logs.name = name
        logs.loginUser = loginUser
        logs.username = username
        logs.status = 'C'
        logs.score = score
        logs.create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logs.save()

def userPool(loginUser,times,acc):
    if times != None:
        global SleepTime
        SleepTime = times


    if acc != None:
        accuracy = acc
    """用户池"""
    while q.empty() == False:

        user = q.get_nowait()
        username = user['username']
        name = user['name']
        print("%s 取出资源 %s" % (loginUser,username))
        userCreate(loginUser,username,name, user['password'],user['user_kecheng'])
def userPoolAddUser(username,name,password,user_kecheng):
    global q
    q.put_nowait({
        "username":username,
        "password":password,
        "name":name,
        "user_kecheng":user_kecheng,
    })
def accuracyUtils(list):
    #accuracy = 50
    print("当前正确率:%s" %accuracy)
    x = len(list) * (accuracy / 100)
    print(int(x))
    for i in range(0,len(list)-int(x)):
        list[i] = None
    return list
if __name__ == '__main__':
    userPoolAddUser("1961001408483","测试111","19900218","思想道德修养与法律基础")
    userPool("test",3,None)



