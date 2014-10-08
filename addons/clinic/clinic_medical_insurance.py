# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class medical_insurance(osv.osv):

    """"""

    _name = 'clinic.medical_insurance'
    _description = 'medical_insurance'

    _columns = {
        'name': fields.char(
            string='Name', required=True, size=64),
        'patient_ids': fields.one2many(
            'res.partner', 'medical_insurance_id', string='patient_ids'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
