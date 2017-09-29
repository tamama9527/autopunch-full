#-*- coding: UTF-8 -*- 
import requests
from BeautifulSoup import BeautifulSoup
import re,json
header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Connection':'keep-alive',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'service002.sds.fcu.edu.tw',
'Referer':'http://service002.sds.fcu.edu.tw/coursequest/',
}
url='http://service002.sds.fcu.edu.tw/coursequest/condition.jsp'
url2='http://service002.sds.fcu.edu.tw/coursequest/student/coursetablebystudent.jsp'
login_data={'Button2':'%B5n%A4J'}
output={}    
s=requests.session()
def sds_class(username,password):
    course_data={'yms_year':'105','yms_smester':'1'}
    login_data['userID']=username
    login_data['userPW']=password
    r=s.post(url,data=login_data,headers=header)
    r=s.post(url2,data=course_data)
    preiod=0
    first_soup=BeautifulSoup(r.text)
    for i in first_soup.findAll('tr',{'class':True}):
        if preiod!=0:
            day=0
            second_soup=BeautifulSoup(str(i))
            for j in second_soup.findAll('td',{'align':True}):
                if day!=0:
                    class_detail= re.findall(u'[\u4E00-\u9FFF\(\)]+[[\u4E00-\u9FFF\w\(\)]+]?',str(j).decode('utf-8'))
                    if class_detail!=[]:
                        time=str(day)+'-'+str(preiod)
                        output[time]={}
                        output[time]['name']=class_detail[0]
                        output[time]['teacher']=class_detail[1]
                        output[time]['location']=class_detail[2]
                day+=1
        preiod +=1
    with open('app/static/course/'+username+'.json', "w") as outfile:
        json.dump(output, outfile, sort_keys = True,indent=4)
    return True
