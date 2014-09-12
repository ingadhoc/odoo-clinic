# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


import re
from openerp import netsvc
from openerp.osv import osv, fields

class clinic_meeting_daily_agenda_wizard(osv.osv_memory):
    _name = 'clinic_meeting_daily_agenda_wizard'
    _description = 'clinic_meeting_daily_agenda_wizard'
    
    _columns = {
        'date': fields.date('Date', required=True),
        'user_ids': fields.many2many('res.users', domain="[('is_medic','=',True)]", string='Medics', required=True),
   }
    
    _defaults = {
    }
    
    def daily_agenda_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids, context=context)[0]
        date = False

        if not context:
            context = {}

        user_ids = [x.id for x in wizard.user_ids]
        datas = {'ids' : user_ids}
        context['date'] = wizard.date
        context['from_wizard'] = True

        return {'type' : 'ir.actions.report.xml',
                         'context' : context,
                         'datas' : datas,
                         'report_name': 'clinic_meeting_daily_agenda'}
        # return {'type' : 'ir.actions.report.xml',
        #                  'context' : context,
        #                  'datas' : datas,
        #                  'report_name': 'clinic_meeting_daily_agenda'}











