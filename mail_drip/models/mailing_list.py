# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MailingSettings(models.Model):
    _inherit = 'mailing.list'

    mail_interval_type = fields.Selection(
        [('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days')],
        string='Mail Interval Type'
    )
    mail_interval = fields.Integer(
        default=0,
        string='Mail Interval'
    )
