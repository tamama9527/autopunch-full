#-*- coding: UTF-8 -*- 
import requests
from PIL import Image
from BeautifulSoup import BeautifulSoup
import time  
from  pytesseract import *
import io
requests.packages.urllib3.disable_warnings()


header={
'Host': 'signin.fcu.edu.tw',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'https://signin.fcu.edu.tw/clockin/login.aspx',
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
}
wifi_header={
'Host': '140.134.18.26',
'Connection': 'keep-alive',
'Content-Length': '47',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Origin': 'http://140.134.18.26',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'DNT':'1',
'Referer': 'http://140.134.18.26/upload/custom/fcu-web/fcu-cp6.htm?cmd=login',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2'
}
login_url='https://signin.fcu.edu.tw/clockin/login.aspx'
Mainpage_url='https://signin.fcu.edu.tw/clockin/Student.aspx'
CheckIn_url='https://signin.fcu.edu.tw/clockin/ClassClockin.aspx'
nid_url='https://tamama.com.tw/xxxxxx'
login_data={'__EVENTTARGET':'','__EVENTARGUMENT':'','LoginLdap$LoginButton':'登入'}
wifi_login='http://140.134.18.25/auth/index.html/u'
wifi_data={
'user':'',
'password':'',
'PtButton':'Logon'
}
Goto_CheckIn={}
CheckIn_data={}
flag=0
#get session and get html hidden form 
def autopunch(username,password):
    s=requests.session()
    first_response=s.get(login_url)
    soup=BeautifulSoup(first_response.text)
    #login and go into main page
    for i in soup.findAll('input',{'type':'hidden','value':True}):
        login_data[str(i['name'])]=str(i['value'])
    login_data['LoginLdap$UserName']=username
    login_data['LoginLdap$Password']=password
    login_response=s.post(login_url,data=login_data,headers=header)
    login_check='您的登入嘗試失敗。請再試一次'
    #您的登入嘗試失敗。請再試一次
    if login_response.text.find(login_check.decode('utf-8')) != -1:
        print '登入失敗'
        return True
    #get hidden form and go into final page
    soup=BeautifulSoup(login_response.text)
    for i in soup.findAll('input',{'type':'hidden','value':True}):
        Goto_CheckIn[str(i['name'])]=str(i['value'])
    Goto_CheckIn['ButtonClassClockin']='學生課堂打卡'
    Mainpage = s.post(Mainpage_url,headers=header,data=Goto_CheckIn)

    #auto send check in data
    soup=BeautifulSoup(Mainpage.text)
    r=s.get('https://signin.fcu.edu.tw/clockin/validateCode.aspx')
    image_file = io.BytesIO(r.content)
    im = Image.open(image_file)
    CheckIn_data['validateCode']=str(image_to_string(im, config='--psm 6 tess.config'))
    print CheckIn_data['validateCode']
    if soup.find('input',{'type':'submit','name':'Button0',})!=None:
        CheckIn_data['Button0'] = soup.find('input',{'type':'submit','name':'Button0',})['value']
    else:
        string=str(username)+'  '+'no class'
        print string
        return True
    for i in soup.findAll('input',{'type':'hidden','value':True}):
        CheckIn_data[str(i['name'])]=str(i['value'])
    result=s.post(CheckIn_url,data=CheckIn_data,headers=header)

    #check the result
    soup=BeautifulSoup(result.text)
    try:
        if soup.find('input',{'type':'submit','name':'Button0'})['disabled']=='disabled':
            string=str(username)+'  '+CheckIn_data['Button0'].encode('utf-8')+'  '+'success'
            print string
            return True
        else:
            print "打卡失敗"
            return True
    except:
        pass
while(True):
    if autopunch('','')==True:
        break
