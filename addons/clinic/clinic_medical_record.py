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


import re
from openerp import netsvc
from openerp.osv import osv, fields

class medical_record(osv.osv):
    """"""
    
    _name = 'clinic.medical_record'
    _description = 'Clinic Medical Record'
    _order = 'date desc'

    _columns = {
        # 'res_id': fields.integer('Related Document ID', readonly=1),
        'user_id': fields.many2one('res.users', 'Medic', required=True),
        'partner_id': fields.many2one('res.partner', 'Patient',),
        'date': fields.date('Date', required=True),
        'body': fields.text('Content', required=True),
        # 'attachment_ids': fields.one2many('ir.attachment', 'res_id', 'Attachments'),
    }

    def _get_default_date(self, cr, uid, context=None):
        return fields.date.context_today(self, cr, uid, context=context)

    _defaults = {
        'user_id': lambda s, cr, u, c: u,
        'date': _get_default_date,
    }


    #------------------------------------------------------
    # download an attachment
    #------------------------------------------------------

#Esto lo saque de mail pero no se para que sirve, lo usariamos para lo deattachmetns

    # def download_attachment(self, cr, uid, id_message, attachment_id, context=None):
    #     """ Return the content of linked attachments. """
    #     message = self.browse(cr, uid, id_message, context=context)
    #     if attachment_id in [attachment.id for attachment in message.attachment_ids]:
    #         attachment = self.pool.get('ir.attachment').browse(cr, SUPERUSER_ID, attachment_id, context=context)
    #         if attachment.datas and attachment.datas_fname:
    #             return {
    #                 'base64': attachment.datas,
    #                 'filename': attachment.datas_fname,
    #             }
    #     return False    
 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
