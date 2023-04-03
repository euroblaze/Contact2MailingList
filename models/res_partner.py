import logging

from odoo import fields, models, api


class MailingContactSubscription(models.Model):
    _inherit = "mailing.contact.subscription"

    @api.constrains('list_id')
    def check_list_id(self):
        for record in self:
            if record.list_id and record.contact_id:
                record.contact_id.write({
                    'list_ids': [(4, record.list_id.id)]
                })

    def unlink(self):
        for record in self:
            if record.list_id and record.contact_id:
                record.contact_id.write({
                    'list_ids': [(3, record.list_id.id)]
                })
                record.contact_id.partner_id.write({
                    'mailing_lists_ids': [(3, record.list_id.id)]
                })
        return super().unlink()

    @api.constrains('contact_id', 'list_id')
    def _check_duplicate(self):
        for record in self:
            if record.contact_id and record.list_id:
                exists = self.search([('contact_id', '=', record.contact_id.id), ('list_id', '=', record.list_id.id)],
                                     limit=1)
                if exists:
                    record.sudo().unlink()


class MailingContact(models.Model):
    _inherit = "mailing.contact"

    partner_id = fields.Many2one('res.partner', required=True)

    @api.onchange('partner_id')
    @api.constrains('partner_id', 'email', 'title')
    def check_partner(self):
        for record in self:
            if record.partner_id and record.partner_id.email != record.email:
                record.email = record.partner_id.email
            if record.partner_id and record.partner_id.title != record.title_id:
                record.title_id = record.partner_id.title


class ResPartner(models.Model):
    _inherit = "res.partner"

    mailings_ids = fields.Many2many('mailing.contact.subscription')
    mailing_lists_ids = fields.Many2many('mailing.list')
    contact = fields.Boolean(compute='_update_contact')

    # def unlink(self):
    #     for record in self:
    #         contact = self.env['mailing.contact'].sudo().search([
    #             ('partner_id', '=', record.id)
    #         ], limit=1)
    #         partners = self.search([('email', '=', contact.email)])
    #         if contact and len(partners) == 1:
    #             contact.unlink()
    #     return super().unlink()

    @api.constrains('title')
    def check_partner(self):
        for record in self:
            contact = self.env['mailing.contact'].sudo().search([
                ('partner_id', '=', record.id)
            ], limit=1)
            if contact:
                contact.title_id = record.title

    def _update_contact(self):
        for record in self:
            contact = self.env['mailing.contact'].sudo().search([
                ('partner_id', '=', record.id)
            ], limit=1)
            check_contact = self.env['mailing.contact'].sudo().search([
                ('email', '=', record.email), '|', ('partner_id', '!=', False), ('partner_id', '=', False)
            ], limit=1)
            if not check_contact.partner_id and check_contact:
                check_contact.write({
                    "partner_id": record.id
                })

            if not contact and not check_contact:
                contact = contact.create({
                    "name": record.name,
                    "email": record.email,
                    "partner_id": record.id,

                })
            elif check_contact:
                contact = check_contact
            record.with_context(skip=True).write({'mailing_lists_ids': [(6, 0, contact.list_ids.ids)]})
            record.with_context(skip=True).write({'mailings_ids': [(6, 0, contact.subscription_list_ids.ids)]})
            record.contact = True

    @api.constrains('mailing_lists_ids')
    def _check_list_id(self):
        if not self.env.context.get("skip"):
            for record in self:
                contact = self.env['mailing.contact'].sudo().search([
                    ('partner_id', '=', record.id)
                ], limit=1)
                check_contact = self.env['mailing.contact'].sudo().search(
                    [('email', '=', record.email), '|', ('partner_id', '!=', False), ('partner_id', '=', False)
                     ], limit=1)
                if not check_contact.partner_id and check_contact:
                    check_contact.write({
                        "partner_id": record.id
                    })
                if not contact and not check_contact:
                    contact = contact.create({
                        "name": record.name,
                        "email": record.email,
                        "partner_id": record.id
                    })
                elif check_contact:
                    contact = check_contact
                contact.list_ids = [(6, 0, record.mailing_lists_ids.ids)]
                for mailinglist in record.mailing_lists_ids:
                    contact_subscription = self.env['mailing.contact.subscription'].sudo().search(
                        [('contact_id', '=', contact.id), ('list_id', '=', mailinglist.id)], limit=1)
                    if not contact_subscription:
                        contact_subscription.create({
                            "contact_id": contact.id,
                            "list_id": mailinglist.id
                        })

    @api.constrains('mailings_ids')
    def _check_mailing_lists(self):
        if not self.env.context.get("skip"):
            for record in self:
                contact = record.env['mailing.contact'].sudo().search([
                    ('partner_id', '=', record.id)
                ], limit=1)
                if contact:
                    for subscription in contact.subscription_list_ids:
                        if subscription.id not in record.mailings_ids.ids:
                            contact.list_ids = [(3, subscription.list_id.id)]
                            record.mailing_lists_ids = [(3, subscription.list_id.id)]
                            subscription.unlink()


class InheritMergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        contact = self.env['mailing.contact'].sudo().search([
            ('partner_id', '=', dst_partner.id)
        ], limit=1)
        contacts = self.env['mailing.contact'].sudo().search([
            ('partner_id', 'in', [p for p in partner_ids if p != dst_partner.id]),
            ('email', '!=', contact.email)
        ])
        super()._merge(partner_ids, dst_partner, extra_checks)
        contacts.sudo().unlink()

