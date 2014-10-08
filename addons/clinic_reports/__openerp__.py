# -*- coding: utf-8 -*-
{   'active': False,
    'author': 'Sistemas ADHOC',
    'category': 'Clinic',
    'depends': [
        'clinic',
        'report_webkit'
        ],
    # 'depends': ['clinic','report_aeroo'],
    # 'depends': ['clinic','report_aeroo','report_aeroo_ooo'],
    'description': """
Clinic Reports
==============
* Clinic Meeting Daily Agenda
""",
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Clinic Reports',
    'test': [],
    'demo': [
    ],
    'data': [ 
            'report/daily_agenda/clinic_meeting_daily_agenda.xml',
            'wizard/clinic_meeting_daily_agenda_wizard_view.xml',
            'data/clinic_reports_data.xml',
            'view/res_users_view.xml',
			'data.xml',
                  ],
    'version': '1.1',
    'website': 'www.sistemasadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
