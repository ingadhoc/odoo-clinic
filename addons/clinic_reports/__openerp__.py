# -*- coding: utf-8 -*-
##############################################################################
#
#    Clinic
#    Copyright (C) 2013 Grupo ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{   'active': False,
    'author': 'Sistemas ADHOC',
    'category': 'Clinic',
    'demo_xml': [],
    'depends': ['clinic','report_webkit'],
    # 'depends': ['clinic','report_aeroo'],
    # 'depends': ['clinic','report_aeroo','report_aeroo_ooo'],
    'description': """
Clinic Reports
==============
* Clinic Meeting Daily Agenda
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Clinic Reports',
    'test': [],
    'demo': [
    ],
    'update_xml': [ 
            'report/daily_agenda/clinic_meeting_daily_agenda.xml',
            'wizard/clinic_meeting_daily_agenda_wizard_view.xml',
            'data/clinic_reports_data.xml',
            'view/res_users_view.xml',
			'data.xml',
                  ],
    'version': '1.1',
    'website': 'www.sistemasadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
