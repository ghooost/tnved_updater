# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

import logging
import zipfile as zf
import tempfile as tf
import os
import time
import re

import base64

#Get the logger
_logger = logging.getLogger(__name__)


class tnvedschedule_wizard(models.TransientModel):
    _name = 'tnvedschedule.wizard'
    upload_file = fields.Binary(string="Upload File")
    clear_before = fields.Boolean(string="Clear table")
    #file_name = fields.Char(string="File Name")

    def extract_zip(self,input_zip):
        input_zip=zf.ZipFile(input_zip)
        return {name: input_zip.read(name) for name in input_zip.namelist()}

    @api.multi
    def button_save(self):
        _logger.info("Start")

        if self.clear_before == True:
            _logger.info("Clear")
            self.env['tnvedschedule.scheduler'].clearItems()

        #_logger.info("Check file ",len(self.upload_file))

        if self.upload_file:
            _logger.info("Got uploaded file")
            f = tf.NamedTemporaryFile(delete=False)
            f.write(base64.decodestring(self.upload_file))
            f.close()

            if f.name:
                unzipped=self.extract_zip(f.name)
                os.remove(f.name)
                found=(0,'')
                for fname,value in unzipped.iteritems():
                    if len(value) > found[0]:
                        found=(len(value),value)

                pro=self.env['tnvedschedule.scheduler']

                if found[0] != 0:
                    pro.openSession()
                    # pat=re.compile('^([\d\s]+)\s+([\d\s]+)\s*\-\s*([^$]+)$')
                    pat=re.compile('^([\d\s]+)\s+\-\s*([^$]+)$')
                    cnt=0
                    body=found[1].decode('cp1251').encode('utf8')
                    for st in body.split('\n'):
                        cnt+=1
                        # if cnt>10:
                        #     break
                        m=pat.search(st)
                        if m:
                            tnv_id=m.group(1).strip()
                            tnv_name=m.group(2).strip()
                            pro.mkItem({'id':tnv_id,'text':tnv_name})

                    _logger.info('Updated: '+str(cnt))
                    pro.closeSession()
                else:
                    _logger.info('No archive found')



        #view_id = self.env.ref('view_scheduler_tree').id
        #menu_id = self.env.ref('default_tnvedschedule_scheduler_menu').id
        model = 'tnvedschedule.scheduler'

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'tree',
            'target': 'current',
            'res_model': model
            #'menu_id':menu_id
            #'view_id': view_id
            # 'res_id': new_price.id,
            # 'flags': {'initial_mode': 'edit'},
        }
