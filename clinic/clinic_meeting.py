# -*- coding: utf-8 -*-
from openerp import tools
from openerp import models, fields, api


class clinic_meeting(models.Model):
    _inherit = 'calendar.event'

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.pool.get(
                'res.partner').browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.pool.get('res.partner').write(
            cr, uid, [id], {'image': tools.image_resize_image_big(value)},
            context=context)

    name = fields.Char(
        default='Turno'
        )
    user_id = fields.Many2one(
        required=True,
        string='Responsible Medic',
        domain="[('is_medic','=',True)]"
        )
    user_partner_ids = fields.Many2many(
        'res.partner',
        compute='get_user_partners',
        )
    user_ids = fields.Many2many(
        'res.users',
        'clinic_meeting_user_rel',
        'meeting_id',
        'user_id',
        string='Attendees',
        states={'done': [('readonly', True)]})
    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        context={'default_is_patient': True},
        domain=[('is_patient', '=', True)],
        )
    room_id = fields.Many2one(
        'clinic.room',
        string='Room',
        required=False)
    mail_sent = fields.Boolean(
        string="Mail Sent"
        )
    image_medium = fields.Binary(
        related='patient_id.image_medium',
        string="Image",
        readonly=True
        )
    duration = fields.Float(
        default='0.5'
        )

    @api.one
    @api.depends(
        'user_ids.partner_id',
        'user_id.partner_id',
        )
    def get_user_partners(self):
        self.user_partner_ids = self.mapped(
            'user_ids.partner_id') + self.user_id.partner_id

    @api.onchange('patient_id')
    def onchange_patient(self):
        if self.patient_id:
            self.user_id = self.patient_id.assigned_medic_id.id
            self.image = self.patient_id.image
            self.image_medium = self.patient_id.image_medium
        else:
            self.user_id = False
            self.image_medium = False

    # def send_mail(self, cr, uid, ids, context):
    #     ir_model_data = self.pool.get('ir.model.data')
    #     template = False
    #     try:
    #         template = ir_model_data.get_object(
    #             cr, uid, 'clinic', 'meeting_alert_email')
    #     except ValueError:
    #         template = False

    #     if not context:
    #         context = {}

    #     for meeting in self.browse(cr, uid, ids, context):
    #         if meeting.patient_id.email:
    #             _logger.debug("Sending reminder to meeting.id %s", meeting.id)
    #             mail_id = self.pool.get('email.template').send_mail(
    #                 cr, uid, template.id, meeting.id, force_send=True, context=context)
    #             self.write(cr, uid, ids, {'mail_sent': True}, context=context)
    #     return True


#     def create(self, cr, uid, vals, context=None):
#         # Corremos el procedimiento padre
#         res = super(clinic_meeting, self).create(cr, uid, vals, context)

#         # mandamos invitacion al patient
#         self.send_invitation(cr, uid, [res], context)
#         return res

#     def write(self, cr, uid, ids, vals, context=None):
#         # Corremos el procedimiento padre
#         res = super(clinic_meeting, self).write(cr, uid, ids, vals, context)

#         # mandamos invitacion al patient
#         self.send_invitation(cr, uid, ids, context)
#         return res

#     def create_attendees(self, cr, uid, ids, context):
# # Cambiamos la tz para el envio de mail
#         # Por ahora definiomos tz del user admin pero se podria mejorar
#         user = self.pool.get('res.users').browse(cr, uid, 1)
#         # user = self.pool.get('res.users').browse(cr, uid, uid)
#         tz = pytz.timezone(user.tz) if user.tz else pytz.utc
#         local_context = dict(context, tz=tz)
#         return super(clinic_meeting, self).create_attendees(cr, uid, ids, local_context)

#     def send_invitation(self, cr, uid, ids, context):
# # Cambiamos la tz para el envio de mail
#         # Por ahora definiomos tz del user admin pero se podria mejorar
#         user = self.pool.get('res.users').browse(cr, uid, 1)
#         # user = self.pool.get('res.users').browse(cr, uid, uid)
#         tz = pytz.timezone(user.tz) if user.tz else pytz.utc
#         local_context = dict(context, tz=tz)

#         att_obj = self.pool.get('calendar.attendee')
#         user_obj = self.pool.get('res.users')
#         current_user = user_obj.browse(cr, uid, uid, context=context)
#         for event in self.browse(cr, uid, ids, context):
#             attendees = {}
#             for att in event.attendee_ids:
#                 attendees[att.partner_id.id] = True
#             new_attendees = []
#             mail_to = ""
#             # for partner in event.partner_ids:
#             if event.patient_id:
#                 partner = event.patient_id
#                 if partner.id in attendees:
#                     continue
#                 # local_context = context.copy()
#                 local_context.pop('default_state', None)
#                 att_id = self.pool.get('calendar.attendee').create(cr, uid, {
#                     'partner_id': partner.id,
#                     'user_id': partner.user_ids and partner.user_ids[0].id or False,
#                     'ref': self._name + ',' + str(event.id),
#                     'email': partner.email
#                 }, context=local_context)
#                 if partner.email:
#                     mail_to = mail_to + " " + partner.email
#                 self.write(cr, uid, [event.id], {
#                     'attendee_ids': [(4, att_id)]
#                 }, context=context)
#                 new_attendees.append(att_id)
#             tz = local_context.get('tz', pytz.timezone('UTC'))

#             if mail_to:
#             # if mail_to and current_user.email:
#                 att_obj._send_mail(cr, uid, new_attendees, mail_to=False,
#                                    email_from=False, context=local_context)
#         return True

    # def list_patients(self, cr, uid, context=None):
    #     ids = self.pool.get('res.partner').search(
    #         cr, uid, [('is_patient', '=', True)])
    #     return self.pool.get('res.partner').name_get(cr, uid, ids, context=context)

    # def list_users(self, cr, uid, context=None):
    #     ids = self.pool.get('res.users').search(
    #         cr, uid, [('is_medic', '=', True)])
    #     return self.pool.get('res.users').name_get(cr, uid, ids, context=context)

    # def get_user_partner(self, cr, uid, user_id, context=None):
    #     user = self.pool.get('res.users').browse(
    #         cr, uid, user_id, context=context)
    #     return user.partner_id.id

# this is a patch for the order by in search and columns of this class and the ones that inherits from this one
# patch from https://bugs.launchpad.net/openobject-addons/+bug/1023322
    # def search(self, cr, uid, args, offset=0, limit=0, order=None, context=None, count=False):
    #     if context is None:
    #         context = {}
    #     new_args = []

    #     for arg in args:
    #         new_arg = arg
    #         if arg[0] in ('date_deadline', unicode('date_deadline')):
    #             if context.get('virtual_id', True):
    #                 new_args += ['|', '&',
    #                              ('recurrency', '=', 1), ('end_date', arg[1], arg[2])]
    #         elif arg[0] == "id":
    #             new_id = get_real_ids(arg[2])
    #             new_arg = (arg[0], arg[1], new_id)
    #         new_args.append(new_arg)
    #     # offset, limit and count must be treated separately as we may need to
    #     # deal with virtual ids
    #     res = super(clinic_meeting, self).search(
    #         cr, uid, new_args, offset=0, limit=0, order=order, context=context, count=False)
    #     if context.get('virtual_id', True):
    #         res = self.get_recurrent_ids(
    #             cr, uid, res, args, limit, context=context)
    #         if order:
    #             order = order.split(',')
    #             sortby = {}
    #             for o in order:
    #                 spl = o.split()
    #                 sortby[spl[0]] = spl[1]
    #             ordered = []
    #             fields = sortby.keys()
    #             for id in res:
    #                 ordered.append(
    #                     self.read(cr, uid, id, fields=fields, context=context))
    #             res = self._multikeysort(ordered, [key.split()[0] if sortby[
    #                                      key.split()[0]] == 'ASC' else '-%s' % key.split()[0] for key in order])
    #             res = [x['id'] for x in res]
    #     if count:
    #         return len(res)
    #     elif limit:
    #         return res[offset:offset + limit]
    #     return res

    # def _multikeysort(self, items, columns):
    #     from operator import itemgetter
    #     comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-')
    #                   else (itemgetter(col.strip()), 1)) for col in columns]

    #     def comparer(left, right):
    #         for fn, mult in comparers:
    #             result = cmp(fn(left), fn(right))
    #             if result:
    #                 return mult * result
    #         else:
    #             return 0
    #     return sorted(items, cmp=comparer)
