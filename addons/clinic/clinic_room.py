# -*- coding: utf-8 -*-
from openerp import models, fields


class room(models.Model):

    """"""

    _name = 'clinic.room'
    _description = 'Room'

    name = fields.Char(
        string='Name', required=True, size=64)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
