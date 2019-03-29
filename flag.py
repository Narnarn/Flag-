#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import fanfou
import re
import shelve

consumer = {'key': '3812d23acfd579969428db1c223141c4', 'secret': '4c6557a19a8b44a1c787937d2a8b657a'}
client = fanfou.XAuth(consumer, 'GetFlag', 'xxxxxx')
fanfou.bound(client)

FlagFile = shelve.open('FlagFile')
FlagFile['ids']=[]
FlagFile['Datas']=[]
#FlagFile['Datas']=[{date:3/21,text:xxxxx,user_id:xxx,name:xx},]

def regex(text):
    fi = re.compile(r'(\d\d|\d)(月|.|-|/)(\d\d|\d)(日|)(.*)',re.DOTALL)
    mo = fi.search(text)
    if not mo:
        return None
    else:
        flag_text = mo.group(5)
        flag_month = mo.group(1) 
        flag_day = mo.group(3)

        if int(flag_month) < 10:
            flag_month = '0'+ str(int(flag_month))           
        if int(flag_day) < 10:
            flag_day = '0'+ str(int(flag_day))           
        flag_date = flag_month + '-' + flag_day
        return (flag_date, flag_text)
    

def add():
    resp = client.statuses.mentions()
    for item in resp.json():
        status_id = item['id']
        if status_id not in FlagFile['ids']:
            FlagFile['ids'].append(status_id)
            
            user_id = item['user']['unique_id']
            name = item['user']['name']
            text = item['text']
            
            temp = regex(text)
            if temp is not None:
                (date, text) = temp
                FlagFile['Datas'].append({'date':date,'text':text,
                                    'user_id':user_id,'name':name})
                body={
                    'status': '@%s flag确认完毕' % name,
                    'in_reply_to_user_id':user_id,
                    }
                #client.statuses.update(body)

                
def reply():
    for things in FlagFile['Datas']:
        if things['date'] == date:
            body={
                'status': '@%s Flag回收ing...您立过flag：今天%s'\
                % (things['name'],things['text']),\
                'in_reply_to_user_id': things['user_id']
                }
            client.statuses.update(body)
            time.sleep(2)


while True:
    date = time.strftime('%m-%d',time.localtime(time.time()))
    now = datetime.datetime.now()
    if now.hour == 22 and now.minute < 1:
        reply()
    elif now.minute % 10 == 0:
        add()

    time.sleep(30)
        
