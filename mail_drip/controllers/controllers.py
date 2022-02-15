# -*- coding: utf-8 -*-
# from odoo import http


# class MailDrip(http.Controller):
#     @http.route('/mail_drip/mail_drip', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mail_drip/mail_drip/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mail_drip.listing', {
#             'root': '/mail_drip/mail_drip',
#             'objects': http.request.env['mail_drip.mail_drip'].search([]),
#         })

#     @http.route('/mail_drip/mail_drip/objects/<model("mail_drip.mail_drip"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mail_drip.object', {
#             'object': obj
#         })
