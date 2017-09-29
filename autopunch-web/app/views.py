# -*- coding: UTF-8 -*-
from flask import render_template, flash, redirect, request, url_for,Response
from flask_login import login_required, login_user
from app import app,login_manager,db
from app.models import user
from form import LoginForm
import os
import hashlib
import time
import json
import check
import sds
import secret
@login_manager.user_loader
def load_user(input_username):
    value_user = user.query.filter(user.username==input_username).first()
    return value_user
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')
@app.route('/')
@app.route('/index')
def index(): 
    name = {'nickname': 'test_server_v1'}  # fake user
    index_title='逢甲打卡小幫手'
    f=open('log.txt','r')
    time=f.readline()
    return render_template("index.html", title = index_title.decode('utf-8'), user = name,time=time)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    temp_username=str(form.account.data).lower()
    temp_password=str(form.password.data)
    if form.validate_on_submit():
        if(check.check(temp_username,temp_password)):
           if db.session.query(user.id).filter_by(username=temp_username).scalar()!=None:
               update_user=db.session.query(user).filter_by(username=temp_username).first()
               if update_user.password!=temp_password:
                   update_user.password=temp_password
                   db.session.commit()
               temp_title='你已經登錄在打卡資料庫中  可以利用cancel來刪除資料'
               return render_template('login_ok.html',user=temp_title.decode('utf-8'))
           else:
               add_user=user(temp_username,temp_password)
               db.session.add(add_user)
               db.session.commit()
               temp_title=temp_username
               return render_template('login_ok.html',user=temp_title.decode('utf-8'))
    return render_template('login.html', form = form)
@app.route('/course', methods=['GET','POST'])
def course():
    if request.method == 'POST':
        temp_username=request.form['username'].lower()
        temp_password=request.form['password']
        filename='app/static/course/'+username+'.json'
        if(check.check(temp_username,temp_password)):
            if db.session.query(user.id).filter_by(username=temp_username).scalar()==None:
                add_user=user(temp_username,temp_password)
                db.session.add(add_user)
                db.session.commit()
            else:
                update_user=db.session.query(user).filter_by(username=temp_username).first()
                if temp_password!=update_user.password:
                    update_user.password=temp_password
                    db.session.commit()
        else:
            return redirect('/course')
        if os.path.isfile(filename)==False:
            sds.sds_class(username,password)
        resp = Response(response=open(filename).read(),status=200,mimetype="application/json")
        return(resp)
    else:
        return "Yo~~~~~ Hacker!"
@app.route('/unpunched',methods=['GET','POST'])
def unpunched():
    if request.method=='POST':
        if hashlib.sha256(request.form['token']).hexdigest()==secret.pw:
            output={}
            index=0
            for i in db.session.query(user).filter().all():
                output[index]={}
                output[index]['username']=i.username
                output[index]['password']=i.password
                index+=1
            db.session.commit()
            nid_ret=json.dumps(output,sort_keys = True ,indent = 4 )
            resp = Response(response=nid_ret,status=200,mimetype="application/json")
            return(resp)
    else:
        return "YO~~~~~~~~~~~"
@app.route('/cancel',methods=['GET','POST'])
def cancel():
    form = LoginForm()
    temp_username=str(form.account.data).lower()
    temp_password=str(form.password.data)
    if form.validate_on_submit():
        if(check.check(temp_username,temp_password)):
           if db.session.query(user.id).filter_by(username=temp_username).scalar()!=None:
               delete_user=db.session.query(user).filter_by(username=temp_username).first()
               db.session.delete(delete_user)    
               temp_title='你已經從打卡資料庫中刪除'
               db.session.commit()
               return render_template('login_ok.html',user=temp_title.decode('utf-8'))
           else:
               temp_title='資料庫沒有你的打卡資料'
               db.session.commit()
               return render_template('login_ok.html',user=temp_title.decode('utf-8'))
    return render_template('cancel_login.html', form = form)
@app.route('/privacy')
def privacy():
    return render_template('privacy.htm')
@app.route('/terms')
def terms():
    return render_template('terms.htm')
@app.route('/time',methods=['GET','POST'])
def time():
    if request.method=='POST':
        f=open('log.txt','w+')
        f.write(request.form['time'])
        f.close()
        return "ok"
    else:
        f=open('log.txt','r')
        time=f.readline()
        f.close()
        return time
