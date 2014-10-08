# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class patient(osv.osv):

    """"""

    _inherit = ['res.partner']

    _columns = {
        'assigned_medic_id': fields.many2one('res.users', string='Assigned Medic', track_visibility='onchange',  domain=[('partner_id.is_medic', '=', True)]),
        'email': fields.char('Email', size=240, track_visibility='onchange'),
        'phone': fields.char('Phone', size=64, track_visibility='onchange'),
        'fax': fields.char('Fax', size=64, track_visibility='onchange'),
        'mobile': fields.char('Mobile', size=64, track_visibility='onchange'),
        'insurance_number': fields.char(string='Insurance Number', size=64, track_visibility='onchange'),
        'facebook': fields.char(string='Facebook', track_visibility='onchange'),
        'skype': fields.char(string='Skype', track_visibility='onchange'),
        'birthday': fields.date(string='Birthday', track_visibility='onchange'),
        'dni': fields.char(string='DNI', size=16, track_visibility='onchange'),
        'html_comment': fields.html(string='Comment', track_visibility='onchange'),
        'medical_insurance_id': fields.many2one('clinic.medical_insurance', string='Medical Insurance', track_visibility='onchange'),
        'is_patient': fields.boolean(string='Patient'),
        # Lo hacemos readonly para que solo pueda ser habilitado desde
        # usuarios, solo users administradores
        'is_medic': fields.boolean(string='Medic', readonly="True"),
        'meeting_ids': fields.one2many('calendar.event', 'patient_id', string='Meetings'),
        'medical_record_ids': fields.one2many('clinic.medical_record', 'partner_id', 'Medical Record',),
    }

#     def _message_get_auto_subscribe_fields(self, cr, uid, updated_fields, auto_follow_fields=['user_id'], context=None):
#         follow_fields = ['assigned_medic_id']
#         follow_fields += auto_follow_fields
#         return super(patient, self)._message_get_auto_subscribe_fields(cr, uid, updated_fields, auto_follow_fields=follow_fields, context=context)

# # Con esto deshabilitamos para que no sugiera hacer seguidor al mismo partner, lo volvi a habilitar porque praecia lo mas logico
#     # def message_get_suggested_recipients(self, cr, uid, ids, context=None):
#         # recipients = []

# #        recipients = super(res_partner_mail, self).message_get_suggested_recipients(cr, uid, ids, context=context)
# #        for partner in self.browse(cr, uid, ids, context=context):
# #            self._message_add_suggested_recipient(cr, uid, recipients, partner, partner=partner, reason=_('Partner Profile'))
#         return recipients

    _defaults = {
        'is_patient': True,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
