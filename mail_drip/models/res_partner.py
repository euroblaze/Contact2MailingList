# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    subscription_list_ids = fields.Many2many('mailing.list', string='Mailing Lists')
