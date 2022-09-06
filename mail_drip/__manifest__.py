{
    'name': "Mail Drip",

    'summary': """
        Mail Drip
    """,

    'description': """
        About Mail Drip
        This module is based on Email Marketing module.
        1. Create mailing lists, add users to them, remove them and delete them.
        2. Create a sequence of emails (Mail Sequence, Msq). The order of emails in each sequence can be changed.
        3. Each mailing list can be assigned to one or more mail-sequences.
        4. Mail-sender triggers at a fixed time every day.
    """,

    'author': "Ivana Bubevska, Bojan Dimovski, Simplify-ERP®",
    'website': "https://simplify-erp.com/",
    'category': 'Mail',
    'version': '1.0',
    'depends': ['mass_mailing'],
    'data': [
        'views/mailing_mailing.xml',
        'views/mailing_contact_subscription.xml',
        'views/mailing_list.xml',
        'views/mailing_cron.xml',
        'views/res_partner.xml',
    ],
}
