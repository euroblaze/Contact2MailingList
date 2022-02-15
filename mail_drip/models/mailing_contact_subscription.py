# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo.http import request
from odoo import models, fields, api


class MailingContact(models.Model):
    _inherit = 'mailing.contact.subscription'

    last_email_sent_date = fields.Datetime(string='Last Email Sent Date', readonly=True,
                                           default=datetime.now(pytz.timezone(request.env.user.tz or pytz.utc)).replace(
                                               tzinfo=None))
    last_email_sent_sequence = fields.Integer(string='Last Email Sent Sequence', readonly=True)
    first_email_sent = fields.Boolean(default=False, string='First email sent in sequence of emails?', readonly=True)