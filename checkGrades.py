import io
import json
import requests
import telebot
jsonfile=json.load(open('/var/odtuclass.json'))
url='https://odtuclass.metu.edu.tr/login/index.php'
telegramToken = ''
bot = telebot.TeleBot(token=telegramToken)
def sendmsg(tex,userid):
    bot.send_message(userid,tex)
for i in jsonfile:
    with requests.Session() as s:
        a=s.get(url)
        resp=a.text
        ind=resp.find('logintoken')
        logstartind=resp.find('"',ind+14)
        logfinisind=resp.find('"',logstartind+1)
        loginToken=resp[logstartind+1:logfinisind]
        loginData={
        'username':jsonfile[i]['username'],
        'password':jsonfile[i]['password'],
        'logintoken':loginToken
        }
        a=s.post(url,data=loginData)

        for j in jsonfile[i]:
            nr='https://odtuclass.metu.edu.tr/course/user.php?id='+j+'&user='+i+'&mode=grade'
            a=s.get(nr)
            tx=a.text
            itemcount=tx.count('gradeitemheader')
            for k in range(itemcount):
                ind=tx.find('gradeitemheader')
                st=tx.find('/>',ind)
                fn=tx.find('<',st)

                gradeid=tx[st+2:fn]


                ind=tx.find(i+' grade')
                st=tx.find('>',ind)
                fn=tx.find('<',st)

                grd=tx[st+1:fn]

                ind=tx.find(i+' average')
                st=tx.find('>',ind)
                fn=tx.find('<',st)

                avg=tx[st+1:fn]

                if gradeid in jsonfile[i][j]['grades']:
                    if jsonfile[i][j]['grades'][gradeid]['grade']!=grd:
                        sendmsg(jsonfile[i][j]['courseName']+'\nItem : '+gradeid+'\nGrade : '+grd+'\nAverage : '+avg,jsonfile[i]['telegram'])
                        jsonfile[i][j]['grades'][gradeid]['grade']=grd
                        jsonfile[i][j]['grades'][gradeid]['average']=avg
                else:
                    jsonfile[i][j]['grades'][gradeid]={}
                    jsonfile[i][j]['grades'][gradeid]['grade']=grd
                    jsonfile[i][j]['grades'][gradeid]['average']=avg
                    if grd!='-':
                        sendmsg(jsonfile[i][j]['courseName']+'\nItem : '+gradeid+'\nGrade : '+grd+'\nAverage : '+avg,jsonfile[i]['telegram'])



                tx=tx[fn:]
with io.open('/var/odtuclass.json', "w", encoding="utf-8") as f:
    f.write(json.dumps(jsonfile))
