# -*- coding: utf-8 -*-
from openerp import models, fields, api
#Import logger
import logging

import time
import requests
import json

#Get the logger
_logger = logging.getLogger(__name__)

#External import
import datetime

class tnvedschedule_scheduler(models.Model):
    _name = 'tnvedschedule.scheduler'
    tnv_id = fields.Char(required=True)
    tnv_name = fields.Text(required=True)
    last_updated = fields.Datetime('Last updated')
    ses_exists=fields.Boolean('Existence in the current session')
    cacheIDS=[]

    #This function is called when the scheduler goes off
    def scheduled_call(self):
        toLoad=['%23']
        loaded=[]
        totalCollection=0
        debugCnt=0

        self.openSession()

        while True:
            needToContinue,toLoad,loaded=self.reLoad(toLoad,loaded)
            time.sleep(5.0)
            debugCnt+=1
            if debugCnt>10:
                _logger.info('break for now')
                print "break for now"
                print "final loop count: %d"%debugCnt
                break

        self.closeSession()

    @api.model
    def openSession(self):
        self.cacheIDS=[i.tnv_id for i in self.search([])]
        #return self.env.search([]).ids
        #self.env.invalidate_all()
        #self.env.cr.execute("update public.tnvedschedule_scheduler set ses_exists=false")
        #self.env.invalidate_all()
        # res=self.search([])
        # for record in res:
        #     record.write({
        #         'ses_exists':False
        #     })
        # return res.id

    @api.model
    def closeSession(self):
        pass
        # self.env.invalidate_all()
        # self.env.cr.execute("update public.tnvedschedule_scheduler set active=false where ses_exists=false")
        # self.env.invalidate_all()
        # res=self.search([('ses_exists','=',False)])
        # for record in res:
        #     record.write({
        #         'active':False
        #     })

    @api.model
    def clearItems(self):
        _logger.info('Clear items')
        self.search([]).unlink()
        _logger.info('Clear items done')

    @api.model
    def mkItem(self,item):
        _logger.info(self.cacheIDS)
        _logger.info(item['id'])
        if item['id'] in self.cacheIDS:
            _logger.info("I'm in, do not do anythong")
            pass
        else:
            _logger.info("Create new item")
            self.create({
                'tnv_id':item['id'],
                'tnv_name':item['text'],
                'last_updated':fields.Datetime.now(),
                'ses_exists':True
            })


        # _logger.info(self.cacheIDS)

    @api.model
    def updateItem(self,item):
        self.create({
            'tnv_id':item['id'],
            'tnv_name':item['text'],
            'last_updated':fields.Datetime.now(),
            'ses_exists':True
        })

        # res=self.search([('tnv_id','=',item['id'])])
        # if len(res)==0:
        #     self.create({
        #         'tnv_id':item['id'],
        #         'tnv_name':item['text'],
        #         'last_updated':fields.Datetime.now(),
        #         'ses_exists':True
        #     })
        # else:
        #     res.write({
        #         'tnv_name':item['text'],
        #         'last_updated':fields.Datetime.now(),
        #         'ses_exists':True
        #     })

    def reLoad(self,toload,loaded):
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
            _logger.info('Load for %s'%itemToLoad)
            r = requests.get('https://tnved.advance-docs.ru/api/v2/codes/?operation=get_node&id='+itemToLoad)
            locLoaded.append(itemToLoad)
            data=r.json()

            _logger.info('will add %i items'%len(data))

            for item in data:
                self.updateItem(item)
                id=item['id']
                if (item['children']) & (id not in loaded+toload+locToLoad):
                    locToLoad.append(id)

        return (needToContinue,toload+locToLoad,loaded+locLoaded)
