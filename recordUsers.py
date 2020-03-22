import json
import requests
import io
import telebot
telegramToken=''
url='https://api.telegram.org/bot'+telegramToken+'/getUpdates'

bot = telebot.TeleBot(token=telegramToken)
def sendmsg(tex,userid):
    bot.send_message(userid,tex)
try:
    jsfile=json.load(open('/var/userlist.json'))
except:
    jsfile={}
a=requests.get(url)
js=a.json()
for i in js['result']:
    userid=i['message']['from']['id']
    userid=str(userid)
    tex=i['message']['text']
    if tex.count(' ')==1 and tex[0]=='e':
        if userid not in jsfile.keys():
            sendmsg('Kayit Basarili',userid)
        jsfile[userid]={}
        jsfile[userid]['user']=tex[:7]
        jsfile[userid]['pass']=tex[8:]
with io.open('/var/userlist.json', "w", encoding="utf-8") as f:
    f.write(json.dumps(jsfile))
