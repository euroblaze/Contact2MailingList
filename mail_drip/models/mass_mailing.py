# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'
    _order = 'sequence asc'

    sequence = fields.Integer(help='Used to order the mails')

    def max_sequence_mailing(self):
        self.env.cr.execute("SELECT MAX(Sequence) FROM mailing_mailing")
        max_sequence = self.env.cr.fetchall()[0][0]
        if not max_sequence:
            max_sequence = 0
        else:
            max_sequence += 1
        return max_sequence

    @api.model
    def create(self, vals):
        record = super(MailingMailing, self).create(vals)
        record.sequence = self.max_sequence_mailing()
        return record

    def unlink(self):
        for record in self:
            mailing_mailing = self.env['mailing.mailing'] \
                .search([('sequence', '>', record.sequence)])
            for mailing in mailing_mailing:
                mailing.write({'sequence': mailing.sequence - 1})
        return super(MailingMailing, self).unlink()
