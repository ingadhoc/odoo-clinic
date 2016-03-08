# -*- coding: utf-8 -*-
{'active': False,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'category': 'Clinic',
    'depends': [
        'mail',
        'calendar',
        'contacts',
        'l10n_ar_states'
    ],
    'description': """
Clinic Module
=============
""",
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Clinic',
    'test': [],
    'demo': [
        # 'data/demo/res.users.csv',
        # 'data/demo/res.company.csv',
        # 'data/demo/clinic.room.csv',
        # 'data/demo/clinic.medical_insurance.csv',
        # 'data/demo/res.partner.csv',
        # 'data/demo/clinic.meeting.xml',
    ],
    'data': [
        'security/clinic_group.xml',
        'security/ir.model.access.csv',
        'view/clinic_menuitem.xml',
        'view/clinic_meeting_view.xml',
        'view/res_partner_view.xml',
        'view/res_users_view.xml',
        'view/clinic_medical_insurance_view.xml',
        'view/clinic_room.xml',
        'view/clinic_medical_record.xml',
        'view/web_calendar.xml',
        # 'data/mail_data.xml',
        'data/clinic_data.xml',
    ],
    'version': '8.0.0.3.0',
 }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
