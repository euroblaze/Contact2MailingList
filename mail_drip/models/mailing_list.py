# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MailingSettings(models.Model):
    _inherit = 'mailing.list'

    mail_interval_type = fields.Selection(
        [('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days')],
        string='Mail Interval Type',
        related='mailing_ids.mail_interval_type'
    )
    mail_interval = fields.Integer(
        default=0,
        string='Mail Interval',
        related='mailing_ids.mail_interval'
    )
    first_mail_datetime = fields.Datetime(
        default=0,
        string='First Mail | Date Hour',
        related='mailing_ids.first_mail_datetime'
    )
    # mailing.list


    def drip_settings(self):
        mailing_view = self.env['mailing.mailing'].search([])
        flag = 1
        res = []
        for mail in mailing_view:
            domain_string = mail.get_mailing_domain()
            name = 'Settings'
            res.append((mail.id, name))
            if str(self.id) in str(domain_string):
                view_id = mail
                flag = 0
        if flag:
            raise UserError("There is no Mailings sent")
        return {
            'res_model': 'mailing.mailing',
            'res_id': view_id.id,
            'res': 'res.append((mail.id, name))',
            'name': _('Settings'),
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('mail_drip.view_mail_mass_mailing_form_drip').id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'context': {'id': self.id}
        }
