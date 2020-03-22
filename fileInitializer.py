import requests
import io
import json
def finduserid(userid,passw):
    url='https://odtuclass.metu.edu.tr/login/index.php'

    with requests.Session() as s:
        a=s.get(url)
        resp=a.text
        ind=resp.find('logintoken')
        logstartind=resp.find('"',ind+14)
        logfinisind=resp.find('"',logstartind+1)
        loginToken=resp[logstartind+1:logfinisind]
        loginData={
        'username':userid,
        'password':passw,
        'logintoken':loginToken
        }
        a=s.post(url,data=loginData)
        a=s.get('https://odtuclass.metu.edu.tr/grade/report/overview/index.php')
        tx=a.text
        ind=tx.find('https://odtuclass.metu.edu.tr/course/user.php?mode=grade&amp;id=')
        lecids=tx.find('id=',ind)
        lecidf=tx.find('&',lecids)
        userst=tx.find('=',lecidf)
        userfi=tx.find('"',userst)
        namest=tx.find('>',ind+1)
        namef=tx.find('<',ind+1)
        namecourse=tx[namest+1:namef]
        courses[tx[lecids+3:lecidf]]={}
        courses[tx[lecids+3:lecidf]]['courseName']=namecourse
        userix=tx[userst+1:userfi]
        return userix
def createjson(userid,passw):
    url='https://odtuclass.metu.edu.tr/login/index.php'

    with requests.Session() as s:
        a=s.get(url)
        resp=a.text
        ind=resp.find('logintoken')
        logstartind=resp.find('"',ind+14)
        logfinisind=resp.find('"',logstartind+1)
        loginToken=resp[logstartind+1:logfinisind]
        loginData={
        'username':userid,
        'password':passw,
        'logintoken':loginToken
        }
        a=s.post(url,data=loginData)
        a=s.get('https://odtuclass.metu.edu.tr/grade/report/overview/index.php')
        tx=a.text
        ind=10
        courses={}
        while ind>0:
            ind=tx.find('https://odtuclass.metu.edu.tr/course/user.php?mode=grade&amp;id=')
            lecids=tx.find('id=',ind)
            lecidf=tx.find('&',lecids)
            userst=tx.find('=',lecidf)
            userfi=tx.find('"',userst)
            namest=tx.find('>',ind+1)
            namef=tx.find('<',ind+1)
            namecourse=tx[namest+1:namef]
            courses[tx[lecids+3:lecidf]]={}
            courses[tx[lecids+3:lecidf]]['courseName']=namecourse
            userix=tx[userst+1:userfi]
            tx=tx[userfi:]
            ind=tx.find('https://odtuclass.metu.edu.tr/course/user.php?mode=grade&amp;id=')
        print(courses)
        for i in courses:
            courses[i]['grades']={}
            nr='https://odtuclass.metu.edu.tr/course/user.php?id='+i+'&user='+userix+'&mode=grade'
            a=s.get(nr)
            tx=a.text
            itemcount=tx.count('gradeitemheader')
            for j in range(itemcount):
                ind=tx.find('gradeitemheader')
                st=tx.find('/>',ind)
                fn=tx.find('<',st)
                gradeid=tx[st+2:fn]
                print(gradeid)
                courses[i]['grades'][gradeid]={}
                ind=tx.find(userix+' grade')
                st=tx.find('>',ind)
                fn=tx.find('<',st)
                grd=tx[st+1:fn]
                courses[i]['grades'][gradeid]['grade']=grd
                ind=tx.find(userix+' average')
                st=tx.find('>',ind)
                fn=tx.find('<',st)
                avg=tx[st+1:fn]
                courses[i]['grades'][gradeid]['average']=avg
                tx=tx[fn:]
    return courses

out={}
userList=json.load(open('/var/userlist.json'))
odtujson=json.load(open('/var/odtuclass.json'))
for i in userList:
    uss=userList[i]['user']
    pss=userList[i]['pass']
    teleg=i
    userix=finduserid(uss,pss)
    if userix not in odtujson:
        courses=createjson(uss,pss)
        odtujson[userix]=courses
        odtujson[userix]['username']=uss
        odtujson[userix]['password']=pss
        odtujson[userix]['telegram']=teleg


with io.open('/var/odtuclass.json', "w", encoding="utf-8") as f:
    f.write(json.dumps(odtujson))
