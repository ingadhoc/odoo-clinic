from openerp import tools, SUPERUSER_ID
import pytz
from datetime import datetime, date, timedelta
from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
@webkit_report_extender("clinic_reports.clinic_meeting_daily_agenda")
def extend_demo(pool, cr, uid, localcontext, context):
    admin = pool.get("res.users").browse(cr, uid, SUPERUSER_ID, context)

    def format_date(date, format):
        format_date = datetime.strftime(date, format)
        return format_date

    def get_date(date):
        if not date:
            date = fields.date.today()
        return date

    def get_medics(user_id):
        from_wizard = localcontext.get('from_wizard', False)
        # If the is asked from a wizard then we only print the agenda for each user choosen in the wizard
        if from_wizard:
            user_ids = [user_id.id]
        else:
            # If the user option is 'all_medics_agenda', then we send all the agenda to this user
            if user_id.daily_schedule_mail == 'all_medics_agenda':            
                user_ids = pool.get("res.users").search(cr, uid, [('is_medic','=',True)])
            else:
                user_ids = [user_id.id]
        user_ids = pool.get("res.users").browse(cr, uid, user_ids)
        return user_ids

    def get_meetings(user_id, date):
        ret = []
        date_from =  datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S")
        date_to = datetime.strftime(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1),'%Y-%m-%d %H:%M:%S')
        meeting_ids = pool.get("calendar.event").search(cr, uid, [('user_id', '=', user_id), ('start', '>=', date_from), ('start', '<', date_to)], order='start ASC')
        meeting = pool.get("calendar.event").browse(cr, uid, meeting_ids)
        ret = meeting
        return ret

    def date_locale (date_time):
        tz = context.get('tz', pytz.timezone('UTC'))
        #res_obj.date and res_obj.date_deadline are in UTC in database so we use context_timestamp() to transform them in the `tz` timezone
        date = fields.datetime.context_timestamp(cr, uid, datetime.strptime(date_time, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
        return date           

    localcontext.update({
        "admin_name": admin.name,
        'get_meetings': get_meetings,
        'get_date': get_date,
        'format_date': format_date,
        'get_medics': get_medics,
        'date_locale': date_locale,
    })
