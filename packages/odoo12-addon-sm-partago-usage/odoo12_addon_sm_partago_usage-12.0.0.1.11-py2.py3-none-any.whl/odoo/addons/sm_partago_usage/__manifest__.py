# -*- coding: utf-8 -*-
{
    'name': "sm_partago_usage",

    'summary': """
        Module to manage reservations from booking app""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.1.11',

    # any module necessary for this one to work correctly
    'depends': ['base', 'vertical_carsharing', 'sm_carsharing_structure'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_cron.xml',
        'views/views_reservation_compute.xml',
        'views/views_edit_reservation_compute_wizard.xml',
        'views/views_wizards.xml',
        'views/views_members.xml'
    ]
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
