# -*- coding: utf-8 -*-
{
    'name': "website whatsapp",

    'summary': """
        Add float Whatsapp link in website""",

    'description': """
        Add float Whatsapp link in website. Configure it from website config
    """,

    'author': "filoquin",
    'website': "http://www.sipecu.com.ar",

    'category': 'website',
    'version': '13.0.1.0.1',
    'depends': ['website'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/templates.xml',
    ],
    'demo': [
        #'demo/demo.xml',
    ],
}
