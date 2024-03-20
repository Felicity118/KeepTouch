from time import sleep
from datetime import date,timedelta
import random
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import numpy as np
from seleniumFunctions import send_message,open_whatsapp,close_driver


scope=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials=ServiceAccountCredentials.from_json_keyfile_name(r'api2.json',scope)
client=gspread.authorize(credentials)
sheet_o=client.open("MichelesFriends").sheet1
sheet=sheet_o.get_all_records()

def get_priority():
    low = 0
    medium = 0
    high = 0
    for s in sheet:
        if s['priority']=='low':
            low+=1
        elif s['priority']=='medium':
            medium+=1
        elif s['priority']=='high':
            high+=1
    return low, medium, high

def date_converter(date):
    l=date.split('-')
    d=l[1]+'/'+l[2]+'/'+l[0]
    return d

text_opt_eng=['Hey {}, how are things going?','Hi {}, anything new going on?','Hey {}, how are you?']
text_opt_ita=['Hey {}, come va?','Oi {}, come stai?']
today=date.today()
open=0
def execute():
    global open
    nextContact_list=[]
    lastContact_list=[]
    for friend in sheet:
        lingua=friend['lingua']
        if lingua=='ita':
            text=random.choice(text_opt_ita)
        elif lingua=='eng':
            text = random.choice(text_opt_eng)
        text = text.format(friend['Nome'])
        nextContact=friend['nextContact']
        if nextContact!='':
            t=nextContact.split('/')
        else:
            nextContact=str(today)
            t = nextContact.split('-')
        low, medium, high = get_priority()
        low_order=[i for i in range(low)]
        medium_order=[m for m in range(medium)]
        high_order=[h for h in range(high)]
        if int(t[2])==today.year and int(t[0])<=today.month and int(t[1])<=today.day:
            if open <1:
                global new_desktop
                new_desktop=open_whatsapp()
                open+=1
            send_message(friend['Numero'],text)
            lastContact_list.append([date_converter(str(today))])
            priority=friend['priority']
            if priority=='high':
                position=int(np.random.choice(high_order,1)[0])
                delta=4+position
                high_order.remove(position)
            elif priority=='medium':
                position = int(np.random.choice(medium_order, 1)[0])
                delta=21+position//2
                medium_order.remove(position)
            else:
                position = int(np.random.choice(low_order, 1)[0])
                delta=60+position//3
                low_order.remove(position)
            nextContact_list.append([date_converter(str(today+ timedelta(days=delta)))])
        else:
            lastContact_list.append([friend['lastContact']])
            nextContact_list.append([friend['nextContact']])
    if open==1:
        number_of_friends=len(sheet)
        last_index='D2:D'+str(number_of_friends+1)
        sheet_o.update(range_name=last_index,values=lastContact_list)
        next_index='E2:E'+str(number_of_friends+1)
        sheet_o.update(range_name=next_index,values=nextContact_list)
    try:
        close_driver()
    except:
        pass
    return open

#execute()










