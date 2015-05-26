# -*- coding: utf-8 -*-
{
    'active': False,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'category': 'Clinic',
    'depends': [
        'clinic',
        'clinic_reports',
        'im_chat',
        'disable_openerp_online',
        'cron_run_manually',
        'document',
    ],
    'description': """
Clinic Project
==============
Installs all modules of Clinic project

Aditional Required configs
--------------------------
On settings/general activate password recovery
Install spanish language
Mod defaul language to es_AR
Set default timezone to 'America/Argentina/Buenos_Aires'

#### ATENCION: se debe utilizar el calendario web de este proyecto y no el nativo de openerp


If reports do not contain headers, install the static version of wkhtmltopdf from https://code.google.com/p/wkhtmltopdf/.
""",
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Clinic Project',
    'test': [],
    'demo': [
    ],
    'data': [
        'data/res_partner_image_data.xml',
        'data/mail_data.xml',
        'data/res_users_data.xml',
        'security/ir.model.access.csv',
        'view/help_view.xml',
        'data/res_company_data.xml',
    ],
    'version': '1.1',
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
