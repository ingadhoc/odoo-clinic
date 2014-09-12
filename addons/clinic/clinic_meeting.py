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

from datetime import datetime, date, timedelta
from openerp import tools, SUPERUSER_ID
import time
import pytz
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _
from ..base_calendar.base_calendar import get_real_ids, base_calendar_id2real_id


class clinic_meeting_type(osv.Model):
    _name = 'clinic.meeting.type'
    _description = 'Clinic Meeting Category'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
    }

class clinic_meeting(osv.Model):
    """"""
    """ Model for clinic_room.pyc meetings """
    _name = 'clinic.meeting'
    _description = "Clinic Meeting"
    _inherit = ["calendar.event", "mail.thread", "ir.needaction_mixin"]
    _order = "date desc"

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.pool.get('res.partner').browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.pool.get('res.partner').write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)            

    _columns = {
        'create_date': fields.datetime('Creation Date', readonly=True),
        'write_date': fields.datetime('Write Date', readonly=True),
        'date_open': fields.datetime('Confirmed', readonly=True),
        'date_closed': fields.datetime('Closed', readonly=True),
        #'partner_ids': fields.many2many('res.partner', 'clinic_meeting_partner_rel', 'meeting_id', 'partner_id',
            # string='Attendees', states={'done': [('readonly', True)]}),
        'user_ids': fields.many2many('res.users', 'clinic_meeting_user_rel', 'meeting_id', 'user_id',
            string='Attendees', states={'done': [('readonly', True)]}),
        'state': fields.selection(
                    [('draft', 'Unconfirmed'), ('open', 'Confirmed')],
                    string='Status', size=16, readonly=True, track_visibility='onchange'),
        # Meeting fields
        'categ_ids': fields.many2many('clinic.meeting.type', 'clinic_meeting_category_rel',
            'event_id', 'type_id', 'Categories'),
        'attendee_ids': fields.many2many('calendar.attendee', 'clinic_meeting_attendee_rel',\
                            'event_id', 'attendee_id', 'Attendees', states={'done': [('readonly', True)]}),
        'patient_id': fields.many2one('res.partner', string='Patient', context={'default_is_patient':True}, domain=[('is_patient','=',True)], required=True), 
        'room_id': fields.many2one('clinic.room', string='Room', required=False), 
        'user_id': fields.many2one('res.users', string='Responsible Medic', domain=[('partner_id.is_medic','=',True)], required=True), 
        'mail_sent': fields.boolean(string="Mail Sent"),        
        'image_medium': fields.related('patient_id', 'image_medium', string="Image", type='binary', readonly=True),
# Todo esto lo comentamos, era para intentar poder cargar la imagen en el calendario tambien pero no pudimos hacerlo andar
        # 'image': fields.related('patient_id', 'image', string="Image", type='binary', store=True,),
        # 'image_medium': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Medium-sized image", type="binary", multi="_get_image",
        #     store={
        #         'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Medium-sized image of this contact. It is automatically "\
        #          "resized as a 128x128px image, with aspect ratio preserved. "\
        #          "Use this field in form views or some kanban views."), 
        # 'image_small': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Small-sized image", type="binary", multi="_get_image",
        #     store={
        #         'res.partner': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Small-sized image of this contact. It is automatically "\
        #          "resized as a 64x64px image, with aspect ratio preserved. "\
        #          "Use this field anywhere a small image is required."),         

        # 'image': fields.related('patient_id', 'image', string="Image", type='binary', store=True),
# Reemplazo description por name porque el campo name es el que se completa desde la vista calendario al crear un nuevo envento y no vi que pueda pasarse como parametro
#IMPORANTE a name no lo reemplazamos porque name es utilizado en varios lugares de base_calendar.py y es obligatorio.         
        # 'name': fields.text('Description', help='Provides a more complete \
                            # description of the calendar component, than that \
                            # provided by the "SUMMARY" property'),     
# Por ahora no lo usamos, ver  "obs duration list en clinic_meeting.py"        
        # 'meeting_duration_id': fields.many2one('clinic.meeting_duration', string="Duration"), 
    }

    _defaults = {
        'user_id': False,
        'duration': '0.5',    
        'state': 'open',   
        'name': 'Turno',     
    }


    _constraints = [
    ]

    def format_date(self, cr, uid, ids, date, format, context):
        # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        format_date = datetime.strftime(date, format)
        return format_date      

    def date_locale (self, cr, uid, ids, date_time, context):
        tz = context.get('tz', pytz.timezone('UTC'))
        #res_obj.date and res_obj.date_deadline are in UTC in database so we use context_timestamp() to transform them in the `tz` timezone
        date = fields.datetime.context_timestamp(cr, uid, datetime.strptime(date_time, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
        return date

    def onchange_patient(self, cr, uid, ids, patient_id):
        v = {}
        
        if patient_id:
            patient_obj = self.pool.get('res.partner')
            patient = patient_obj.browse(cr, uid, patient_id)
            
            if not patient:
                return {'value': v}
            
            if isinstance(patient, list):
                patient = patient[0]
            v['user_id'] = patient.assigned_medic_id.id
            # v['image'] = patient.image
            v['image_medium'] = patient.image_medium
        else:
            v['user_id'] = False       
            # v['image'] = False       
            v['image_medium'] = False       
        return {'value': v}

    def send_mail(self, cr, uid, ids, context):
        ir_model_data = self.pool.get('ir.model.data')
        template = False
        try:
            template = ir_model_data.get_object(cr, uid, 'clinic', 'meeting_alert_email')
        except ValueError:
            template = False

        if not context:
            context = {}

        for meeting in self.browse(cr, uid, ids, context):
            if meeting.patient_id.email:
                _logger.debug("Sending reminder to meeting.id %s", meeting.id)
                mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, meeting.id, force_send=True, context=context)
                self.write(cr, uid, ids, {'mail_sent': True}, context=context)
        return True

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default['attendee_ids'] = False
        return super(clinic_meeting, self).copy(cr, uid, id, default, context)

    # shows events of the day for this user
    def _needaction_domain_get(self, cr, uid, context=None):
        return [('date', '<=', time.strftime(DEFAULT_SERVER_DATE_FORMAT + ' 23:59:59')), ('date_deadline', '>=', time.strftime(DEFAULT_SERVER_DATE_FORMAT + ' 23:59:59')), ('user_id', '=', uid)]

    def message_post(self, cr, uid, thread_id, body='', subject=None, type='notification',
                        subtype=None, parent_id=False, attachments=None, context=None, **kwargs):
        if isinstance(thread_id, str):
            thread_id = get_real_ids(thread_id)
        return super(clinic_meeting, self).message_post(cr, uid, thread_id, body=body, subject=subject, type=type, subtype=subtype, parent_id=parent_id, attachments=attachments, context=context, **kwargs)


    def create(self, cr, uid, vals, context=None):
        # Corremos el procedimiento padre
        res = super(clinic_meeting, self).create(cr, uid, vals, context)
        
        # mandamos invitacion al patient
        self.send_invitation(cr, uid, [res], context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        # Corremos el procedimiento padre
        res = super(clinic_meeting, self).write(cr, uid, ids, vals, context)

        # mandamos invitacion al patient
        self.send_invitation(cr, uid, ids, context)      
        return res        

    def create_attendees(self, cr, uid, ids, context):
# Cambiamos la tz para el envio de mail
        # Por ahora definiomos tz del user admin pero se podria mejorar
        user = self.pool.get('res.users').browse(cr, uid, 1)
        # user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        local_context = dict(context,tz=tz)
        return super(clinic_meeting, self).create_attendees(cr, uid, ids, local_context)

        
    def send_invitation(self, cr, uid, ids, context):
# Cambiamos la tz para el envio de mail
        # Por ahora definiomos tz del user admin pero se podria mejorar
        user = self.pool.get('res.users').browse(cr, uid, 1)
        # user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        local_context = dict(context,tz=tz)

        att_obj = self.pool.get('calendar.attendee')
        user_obj = self.pool.get('res.users')
        current_user = user_obj.browse(cr, uid, uid, context=context)
        for event in self.browse(cr, uid, ids, context):
            attendees = {}
            for att in event.attendee_ids:
                attendees[att.partner_id.id] = True
            new_attendees = []
            mail_to = ""        
            # for partner in event.partner_ids:
            if event.patient_id:
                partner = event.patient_id
                if partner.id in attendees:
                    continue
                # local_context = context.copy()
                local_context.pop('default_state', None)
                att_id = self.pool.get('calendar.attendee').create(cr, uid, {
                    'partner_id': partner.id,
                    'user_id': partner.user_ids and partner.user_ids[0].id or False,
                    'ref': self._name+','+str(event.id),
                    'email': partner.email
                }, context=local_context)
                if partner.email:
                    mail_to = mail_to + " " + partner.email
                self.write(cr, uid, [event.id], {
                    'attendee_ids': [(4, att_id)]
                }, context=context)
                new_attendees.append(att_id)
            tz = local_context.get('tz', pytz.timezone('UTC'))

            if mail_to:
            # if mail_to and current_user.email:
                att_obj._send_mail(cr, uid, new_attendees, mail_to=False,
                    email_from = False, context=local_context)
        return True    

    def list_patients(self, cr, uid, context=None):
        ids = self.pool.get('res.partner').search(cr,uid,[('is_patient','=',True)])
        return self.pool.get('res.partner').name_get(cr, uid, ids, context=context)

    def list_users(self, cr, uid, context=None):
        ids = self.pool.get('res.users').search(cr,uid,[('is_medic','=',True)])
        return self.pool.get('res.users').name_get(cr, uid, ids, context=context)

    def get_user_partner(self, cr, uid, user_id, context=None):
        user = self.pool.get('res.users').browse(cr, uid, user_id, context=context)
        return user.partner_id.id

# this is a patch for the order by in search and columns of this class and the ones that inherits from this one
# patch from https://bugs.launchpad.net/openobject-addons/+bug/1023322
    def search(self, cr, uid, args, offset=0, limit=0, order=None, context=None, count=False):
        if context is None:
            context = {}
        new_args = []

        for arg in args:
            new_arg = arg
            if arg[0] in ('date_deadline', unicode('date_deadline')):
                if context.get('virtual_id', True):
                    new_args += ['|','&',('recurrency','=',1),('end_date', arg[1], arg[2])]
            elif arg[0] == "id":
                new_id = get_real_ids(arg[2])
                new_arg = (arg[0], arg[1], new_id)
            new_args.append(new_arg)
        #offset, limit and count must be treated separately as we may need to deal with virtual ids
        res = super(clinic_meeting, self).search(cr, uid, new_args, offset=0, limit=0, order=order, context=context, count=False)
        if context.get('virtual_id', True):
            res = self.get_recurrent_ids(cr, uid, res, args, limit, context=context)
            if order:
                order = order.split(',')
                sortby = {}
                for o in order:
                    spl = o.split()
                    sortby[spl[0]] = spl[1]
                ordered = []
                fields = sortby.keys()
                for id in res:
                    ordered.append(self.read(cr, uid, id, fields=fields, context=context))
                res = self._multikeysort(ordered, [key.split()[0] if sortby[key.split()[0]] == 'ASC' else '-%s' % key.split()[0] for key in order])
                res = [x['id'] for x in res]            
        if count:
            return len(res)
        elif limit:
            return res[offset:offset+limit]
        return res
    
    def _multikeysort(self, items, columns):
        from operator import itemgetter
        comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]
        def comparer(left, right):
            for fn, mult in comparers:
                result = cmp(fn(left), fn(right))
                if result:
                    return mult * result
            else:
                return 0
        return sorted(items, cmp=comparer)

# In open trunk it gives an error. I think this should be neccesary only for recurring events (look for 'base_calendar_id2real_id' in base_calendar.py)
    # def message_get_subscription_data(self, cr, uid, ids, context=None):
    #     res = {}
    #     for virtual_id in ids:
    #         real_id = base_calendar_id2real_id(virtual_id)
    #         result = super(clinic_meeting, self).message_get_subscription_data(cr, uid, [real_id], context=context)
    #         res[virtual_id] = result[real_id]
    #     return res

# Por ahora no lo usamos, ver  "obs duration list en clinic_meeting.py"
    # def onchange_meeting_duration_id(self, cr, uid, ids, meeting_duration_id, date, duration, False, allday, context=None):
       
    #     v = {}

    #     if meeting_duration_id:       
    #         meeting_duration_obj = self.pool.get('clinic.meeting_duration')
    #         meeting_duration = meeting_duration_obj.browse(cr, uid, meeting_duration_id, context=context)
            
    #         if not meeting_duration:
    #             return {'value': v}
            
    #         if isinstance(meeting_duration, list):
    #             meeting_duration = meeting_duration[0]
    #         v['duration'] = meeting_duration.name
    #     else:
    #         v['duration'] = False
        
    #     return {'value': v}


# No termine esta funcion ver "obs duration list"
    # def onchange_dates(self, cr, uid, ids, start_date, duration=False, end_date=False, allday=False, context=None):
        
    #     v = super(clinic_meeting, self).onchange_dates(cr, uid, ids, start_date, duration, end_date, allday, context=context)
    #     if duration:
    #         meeting_duration_obj = self.pool.get('clinic.meeting_duration')
    #         meeting_duration = meeting_duration_obj.browse(cr, uid, meeting_duration_id, context=context)                     
    #         v['meeting_duration_id'] = meeting_duration.name
    #     # llamar funcion padre
    #     # hacer que meeting_duration_id tome el valor de duration

    #     return {'value': v}


############## 
# "obs duration list"
# si hago el campo duration un campo m2o da errores porque hay funciones onchange y demás que dan errores
# la vista calendario requiere de un campo que exprese la duracion float o integer en "date_delay", no se puede sacar
# La parte que fue casi imposible de resolver es que desde el widget calendario, yo pueda elegir una determinada cantidad de hroas y eso me elija la hora correspondiente en la lista desplegable. Se piensa que esta función no es importante

    # def list_periods(self, cr, uid, context=None):
    #     ids = self.pool.get('account.period').search(cr,uid,[])
    #     return self.pool.get('account.period').name_get(cr, uid, ids, context=context)