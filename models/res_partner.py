from odoo import fields, models, api


class MailingContact(models.Model):
    _inherit = "mailing.contact"

    partner_id = fields.Many2one('res.partner', required=True)


class ResPartner(models.Model):
    _inherit = "res.partner"

    mailings_ids = fields.Many2many('mailing.contact.subscription')
    mailing_lists_ids = fields.Many2many('mailing.list')
    contact = fields.Boolean(compute='_update_contact')

    def _update_contact(self):
        for record in self:
            contact = self.env['mailing.contact'].sudo().search([
                ('partner_id', '=', record.id)
            ], limit=1)

            if not contact:
                contact = contact.create({
                    "name": record.name,
                    "email": record.email,
                    "partner_id": record.id,

                })
            record.mailing_lists_ids = [(6, 0, contact.list_ids.ids)]
            record.mailings_ids = [(6, 0, contact.subscription_list_ids.ids)]
            record.contact = True

    @api.constrains('mailing_lists_ids')
    def _check_list_id(self):
        for record in self:
            contact = self.env['mailing.contact'].sudo().search([
                ('partner_id', '=', record.id)
            ], limit=1)
            if not contact:
                contact = contact.create({
                    "name": record.name,
                    "email": record.email,
                    "partner_id": record.id
                })
            contact.list_ids = [(6, 0, record.mailing_lists_ids.ids)]
            for mailinglist in record.mailing_lists_ids:
                contact_subscription = self.env['mailing.contact.subscription'].sudo().search(
                    [('contact_id', '=', contact.id), ('list_id', '=', mailinglist.id)], limit=1)
                if not contact_subscription:
                    contact_subscription.create({
                        "contact_id": contact.id,
                        "list_id": mailinglist.id
                    })
