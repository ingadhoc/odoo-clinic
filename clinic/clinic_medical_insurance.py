# -*- coding: utf-8 -*-
from openerp import models, fields


class medical_insurance(models.Model):
    """"""

    _name = 'clinic.medical_insurance'
    _description = 'medical_insurance'

    name = fields.Char(
        string='Name', required=True, size=64)
    patient_ids = fields.One2many(
        'res.partner', 'medical_insurance_id', string='patient_ids')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
