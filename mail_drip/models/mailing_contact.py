# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.http import request


class MailingContact(models.Model):
    _inherit = 'mailing.contact'

    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.onchange('partner_id')
    def save_partner_data(self):
        for record in self:
            if record.partner_id:
                record.name = record.partner_id.name
                record.email = record.partner_id.email
                record.title_id = record.partner_id.title.id

    @api.constrains('subscription_list_ids')
    def send_first_mail_in_sequence(self):
        mails = self.env['mailing.mailing'].search([])
        for record in self:
            for subscription in record.subscription_list_ids:
                if subscription.list_id != subscription.last_sent_mailing_list:
                    subscription.first_email_sent = False
                    subscription.last_sent_mailing_list = subscription.list_id.id
                if not subscription.first_email_sent:
                    mails_to_send = mails.filtered(lambda l: subscription.list_id.id in l.contact_list_ids.ids) \
                        .sorted(key='sequence', reverse=False)
                    if len(mails_to_send) >= 1:
                        mail_to_send = mails_to_send[0]
                        mail_values = {
                            "subject": mail_to_send.subject,
                            "email_from": self.env.user.email_formatted,
                            "email_to": record.email,
                            "body_html": mail_to_send.body_arch,
                            'state': 'outgoing'
                        }
                        mail = self.env["mail.mail"].create(mail_values)
                        mail.send(raise_exception=False)
                        user_tz = request.env.user.tz or pytz.utc
                        subscription.last_email_sent_date = datetime.now(pytz.timezone(user_tz)).replace(
                            tzinfo=None)
                        subscription.last_email_sent_sequence = 0
                        subscription.first_email_sent = True

    @api.model
    def mail_cron_job(self):
        mailing_contacts = self.env['mailing.contact'].search([])
        mails = self.env['mailing.mailing'].search([])
        for contact in mailing_contacts:
            for subscription in contact.subscription_list_ids:
                first_mail_time = subscription.list_id.first_mail_datetime
                result = None
                type_time = subscription.list_id.mail_interval_type
                time = subscription.list_id.mail_interval
                last_email_sent_date = subscription.last_email_sent_date
                sequence = subscription.last_email_sent_sequence + 1
                if time and time > 0 and type_time and last_email_sent_date:
                    if type_time == 'minutes':
                        result = last_email_sent_date + timedelta(minutes=time)
                    elif type_time == 'hours':
                        result = last_email_sent_date + timedelta(hours=time)
                    elif type_time == 'days':
                        result = last_email_sent_date + timedelta(days=time)
                    user_tz = request.env.user.tz or pytz.utc
                    date_now = datetime.now(pytz.timezone(user_tz)).replace(tzinfo=None)
                    if first_mail_time == date_now:
                        if result <= date_now:
                            mails_to_send = mails.filtered(lambda l: subscription.list_id.id in l.contact_list_ids.ids) \
                                .sorted(key='sequence', reverse=False)
                            if len(mails_to_send) - 1 >= sequence:
                                mail_to_send = mails_to_send[sequence]
                                mail_values = {
                                    "subject": mail_to_send.subject,
                                    "email_from": mails_to_send.email_from,
                                    "reply_to": mails_to_send.reply_to,
                                    "email_to": contact.email,
                                    "body_html": mail_to_send.body_arch,
                                    'state': 'outgoing',
                                }
                                mail = self.env["mail.mail"].create(mail_values)
                                mail.send(raise_exception=False)
                                subscription.last_email_sent_date = datetime.now(pytz.timezone(user_tz)).replace(
                                    tzinfo=None)
                                subscription.last_email_sent_sequence = sequence
