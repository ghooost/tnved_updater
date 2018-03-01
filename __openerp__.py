# -*- coding: utf-8 -*-
{
    'name': "tnvedschedule",

    'summary': """
        TNVED downloader
    """,

    'description': """
    """,

    'author': "AdvanceDocs",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
	#'data/scheduler.xml',
    'data': [
	'views/views.xml'
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
