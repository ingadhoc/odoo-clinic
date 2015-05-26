from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)


class res_users(osv.osv):

    """"""

    _inherit = 'res.users'

    _columns = {
        'daily_schedule_mail': fields.selection([('never', 'Never'), ('my_agenda', 'My Agenda'), ('all_medics_agenda', 'All Medics Agenda')],
                                                string='Receive Daily Agenda', size=32, required=True,),
    }

    _defaults = {
        'daily_schedule_mail': lambda *args: 'never'
    }

    def cron_user_daily_agenda(self, cr, uid, context=None):
        if context is None:
            context = {}

        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(
                cr, uid, 'clinic_reports', 'meeting_daily_agenda_email')
        except ValueError:
            template = False

        ids = self.search(cr, uid, [])
        for user_id in self.browse(cr, uid, ids):
            if user_id.daily_schedule_mail != 'never' and user_id.email:
                _logger.debug("Sending reminder to uid %s", user_id.id)
                self.pool.get('email.template').send_mail(
                    cr, uid, template.id, user_id.id, force_send=True, context=context)
        return True

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.extend(['daily_schedule_mail'])
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.extend(['daily_schedule_mail', ])
        return init_res
