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
    'depends': ['mail', 'base_calendar', 'contacts', 'l10n_ar_states'],
    'description': """
Clinic Module
============= 
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Clinic',
    'test': [],
    'demo': [
      'data/demo/res.users.csv',
      'data/demo/res.company.csv',
      'data/demo/clinic.room.csv',
      'data/demo/clinic.medical_insurance.csv',
      'data/demo/res.partner.csv',
      # dejamos de usar el csv porque no sabia como pasar el eval de la fecha, usamos el .xml
      # 'data/demo/clinic.meeting.csv',
      'data/demo/clinic.meeting.xml',
    ],
    'update_xml': [   
      'security/clinic_group.xml',
      'security/ir.model.access.csv',
      'view/clinic_menuitem.xml',
      'view/clinic_meeting_view.xml',
      'view/res_partner_view.xml',
      'view/res_users_view.xml',
      'view/clinic_medical_insurance_view.xml',
      'view/clinic_room.xml',
      'view/clinic_meeting_type_view.xml',
      # Por ahora no lo usamos, ver  "obs duration list en clinic_meeting.py"      
      # 'view/clinic_meeting_duration_view.xml',
      'view/clinic_medical_record.xml',
      'data/mail_data.xml',
      'data/clinic_data.xml',
                  ],
    'version': '1.1',
    'website': 'www.sistemasadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
