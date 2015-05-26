# -*- coding: utf-8 -*-
from openerp import models, fields


class medical_record(models.Model):
    """"""

    _name = 'clinic.medical_record'
    _description = 'Clinic Medical Record'
    _order = 'date desc'

    user_id = fields.Many2one(
        'res.users', 'Medic', required=True, default=lambda self: self.env.user
        )
    partner_id = fields.Many2one(
        'res.partner', 'Patient'
        )
    date = fields.Date(
        'Date', required=True, default=fields.Date.context_today,
        )
    body = fields.Text(
        'Content', required=True
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
