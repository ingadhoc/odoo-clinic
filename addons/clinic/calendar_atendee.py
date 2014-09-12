from datetime import datetime, timedelta, date
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from openerp import tools, SUPERUSER_ID
import openerp.service.report
from openerp.osv import fields, osv
from openerp.tools.translate import _
import pytz
import re
import time

import logging
_logger = logging.getLogger(__name__)

class calendar_attendee(osv.osv):
    """
    Calendar Attendee Information
    """
    _inherit = 'calendar.attendee'

    def _send_mail(self, cr, uid, ids, mail_to, email_from=False, context=None):
    # def _send_mail(self, cr, uid, ids, mail_to, email_from=tools.config.get('email_from', False), context=None):
        """
        Send mail for event invitation to event attendees.
        @param email_from: email address for user sending the mail
        @return: True
        """
        
        # Get html_invitation
        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'clinic', 'meeting_invitation')
        except ValueError:
            template = False
        if not template:
            raise osv.except_osv(_('No template email defined!'), ("There is no template email defined for model calendar.atendee"))

        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.name
        for att in self.browse(cr, uid, ids, context=context):
            res_obj = att.ref
            if res_obj:
                # Generacion de valores para el email a partir del email template
                vals = self.pool.get('email.template').generate_email(cr, uid, template.id, att.id, context=context)
                # tz = context.get('tz', pytz.timezone('UTC'))
                #res_obj.date and res_obj.date_deadline are in UTC in database so we use context_timestamp() to transform them in the `tz` timezone
                date_start = fields.datetime.context_timestamp(cr, uid, datetime.strptime(res_obj.date, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
                date_stop = False
                ics_file = self.get_ics_file(cr, uid, res_obj, context=context)
                if ics_file:
                    vals['attachment_ids'] = [(0,0,{'name': 'invitation.ics',
                                                    'datas_fname': 'invitation.ics',
                                                    'datas': str(ics_file).encode('base64')})]
                msg_id = self.pool.get('mail.mail').create(cr, uid, vals, context=context)
                # Lo deshabilitamos para que sea mas rapido cuando se guarda un nuevo evento
                # self.pool.get('mail.mail').send(cr, uid, [msg_id], context=context)
            return True

    # def date_locale (self, cr, uid, ids, date_time, context):
    #     tz = context.get('tz', pytz.timezone('UTC'))
    #     #res_obj.date and res_obj.date_deadline are in UTC in database so we use context_timestamp() to transform them in the `tz` timezone
    #     print 'default tmz!'
    #     print tools.DEFAULT_SERVER_DATETIME_FORMAT
    #     print date_time
    #     date = fields.datetime.context_timestamp(cr, uid, datetime.strptime(date_time, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
    #     return date
    
    def date_locale (self, cr, uid, ids, date_time, context):
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')        
        # tomamos la timezone del super user
        user = self.pool.get('res.users').browse(cr, uid, SUPERUSER_ID)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        date = pytz.utc.localize(date_time).astimezone(tz)
        return date        

    def format_date(self, cr, uid, ids, date, format, context):
        format_date = datetime.strftime(date, format)
        return format_date        