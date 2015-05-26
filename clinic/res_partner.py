# -*- coding: utf-8 -*-
from openerp import models, fields


class partner(models.Model):
    """"""

    _inherit = 'res.partner'

    assigned_medic_id = fields.Many2one(
        'res.users',
        string='Assigned Medic',
        track_visibility='onchange',
        domain=[('partner_id.is_medic', '=', True)]
        )
    insurance_number = fields.Char(
        string='Insurance Number',
        track_visibility='onchange'
        )
    html_comment = fields.Html(
        string='Comment',
        track_visibility='onchange'
        )
    medical_insurance_id = fields.Many2one(
        'clinic.medical_insurance',
        string='Medical Insurance',
        track_visibility='onchange'
        )
    is_patient = fields.Boolean(
        string='Patient',
        default=True,
        )
    # Lo hacemos readonly para que solo pueda ser habilitado desde usuarios,
    # solo users administradores
    is_medic = fields.Boolean(
        string='Medic',
        readonly="True"
        )
    meeting_ids = fields.One2many(
        'calendar.event',
        'patient_id',
        string='Meetings'
        )
    medical_record_ids = fields.One2many(
        'clinic.medical_record',
        'partner_id',
        'Medical Record'
        )
    # add track visiblity
    email = fields.Char(
        track_visibility='onchange'
        )
    phone = fields.Char(
        track_visibility='onchange'
        )
    fax = fields.Char(
        track_visibility='onchange'
        )
    mobile = fields.Char(
        track_visibility='onchange'
        )
# Fields to analize
    facebook = fields.Char(
        string='Facebook',
        track_visibility='onchange'
        )
    skype = fields.Char(
        string='Skype',
        track_visibility='onchange'
        )
    birthday = fields.Date(
        string='Birthday',
        track_visibility='onchange'
        )
    dni = fields.Char(
        string='DNI',
        size=16,
        track_visibility='onchange'
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
