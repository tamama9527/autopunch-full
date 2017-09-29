#-*- coding: UTF-8 -*- 
import requests
from BeautifulSoup import BeautifulSoup

header={
'Host': 'signin.fcu.edu.tw',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'https://signin.fcu.edu.tw/clockin/login.aspx',
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
}
login_url='https://signin.fcu.edu.tw/clockin/login.aspx'
Mainpage_url='https://signin.fcu.edu.tw/clockin/Student.aspx'
CheckIn_url='https://signin.fcu.edu.tw/clockin/ClassClockin.aspx'
login_data={'__EVENTTARGET':'','__EVENTARGUMENT':'','LoginLdap$LoginButton':'登入'}
#get session and get html hidden form
def check(username,password):
    s=requests.session()
    first_response=s.get(login_url)
    soup=BeautifulSoup(first_response.text)
    #login and go into main page
    for i in soup.findAll('input',{'type':'hidden','value':True}):
        login_data[str(i['name'])]=str(i['value'])
    login_data['LoginLdap$UserName']=username
    login_data['LoginLdap$Password']=password
    login_response=s.post(login_url,data=login_data,headers=header)
    login_check='您的登入嘗試失敗。請再試一次。'
    #您的登入嘗試失敗。請再試一次
    if login_response.text.find(login_check.decode('utf-8')) != -1:
        return False
    else:
        return True
