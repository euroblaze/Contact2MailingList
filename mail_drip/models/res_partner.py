# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo.http import request
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    subscription_list_ids = fields.Many2many('mailing.list', string='Mailing Lists')
