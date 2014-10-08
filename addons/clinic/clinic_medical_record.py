# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class medical_record(osv.osv):

    """"""

    _name = 'clinic.medical_record'
    _description = 'Clinic Medical Record'
    _order = 'date desc'

    _columns = {
        'user_id': fields.many2one('res.users', 'Medic', required=True),
        'partner_id': fields.many2one('res.partner', 'Patient',),
        'date': fields.date('Date', required=True),
        'body': fields.text('Content', required=True),
    }

    def _get_default_date(self, cr, uid, context=None):
        return fields.date.context_today(self, cr, uid, context=context)

    _defaults = {
        'user_id': lambda s, cr, u, c: u,
        'date': _get_default_date,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
