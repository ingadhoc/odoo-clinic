# -*- coding: utf-8 -*-
{   'active': False,
    'author': 'Sistemas ADHOC',
    'category': 'Clinic',
    'depends': [
        'clinic',
        'clinic_reports',
        'im_chat',
        # 'web_nocreatedb',
        'disable_openerp_online',
        # 'cron_run_manually',
        # 'web_clinic_cust',
        'document',
        ],
    # 'depends': ['clinic', 'clinic_reports','im', 'web_nocreatedb','web_m2o_enhanced', 'disable_openerp_online'],
    'description': """
Clinic Project
============== 
Installs all modules of Clinic project

Aditional Required configs
--------------------------
On settings/genral activate password recovery
Install spanish language
Mod defaul language to es_AR
Set default timezone to 'America/Argentina/Buenos_Aires'



MOD: removed dependency to web_m2o_enhaced becouse it doesn't works ok on trunk or saas-2
We make it dependet on 'web_m2o_enhanced' so that you can limit the creation of records in m2o fields but it isn't really required. 
You can find this module in in https://github.com/0k/web_m2o_enhanced.git

#### ATENCION: se debe utilizar el calendario web de este proyecto y no el nativo de openerp

Projects required:
* https://github.com/0k/web_m2o_enhanced.git
* lp:~sistemas-adhoc/openerp-l10n-ar-localization/7.0
* lp:server-env-tools/7.0 --> disable_openerp_online
* lp:web-addons/7.0 --> web_nocreatedb,

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
            'data/res_company_data.xml',
            #regla agregada para permitir que se borren documentos
                  ],
    'version': '1.1',
    'application': True,
    'website': 'www.sistemasadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
