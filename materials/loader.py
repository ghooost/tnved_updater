# -*- coding: utf-8 -*-
import time
import requests
import json

toLoad=['%23']
loaded=[]
totalCollection=0
debugCnt=0
fileToSave=False

def doSomething(item):
    #totalCollection+=1
    pass

def formFileName(id):
    if id=='%23':
        return 'data/_start.json'
    return 'data/'+str(id)+'.json'

def reLoad(toload,loaded,doSomething):
    needToContinue=False
    locToLoad=[]
    locLoaded=[]
    itemToLoad=False
    for i in toload:
        if i not in loaded:
            itemToLoad=str(i)
            break

    if itemToLoad!=False:
        needToContinue=True
        print 'Load for %s'%itemToLoad
        r = requests.get('https://tnved.advance-docs.ru/api/v2/codes/?operation=get_node&id='+itemToLoad)
        locLoaded.append(itemToLoad)
        data=r.json()

        with open(formFileName(itemToLoad),'w') as fileToSave:
            fileToSave.write(json.dumps(data))

        for item in data:
            doSomething(item)
            id=item['id']
            if (item['children']) & (id not in loaded+toload+locToLoad):
                locToLoad.append(id)
    return (needToContinue,toload+locToLoad,loaded+locLoaded)

while True:
    needToContinue,toLoad,loaded=reLoad(toLoad,loaded,doSomething)
    print needToContinue,len(toLoad),len(loaded)
    time.sleep(2.0)
    debugCnt+=1
    if debugCnt>3:
        print "break for now"
        print "final loop count: %d"%debugCnt
        break
