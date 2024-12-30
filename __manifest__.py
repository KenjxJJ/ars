# -*- coding: utf-8 -*-
{
    'name': "Airport Reservation System",

    'summary': """
            Management System for Booking Processing in Airline Services.
        """,

    'description': """
    """,

    'author': "KenjxJJ",

    'category': 'Fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ars_passenger_views.xml',
        'views/ars_ticket_views.xml',
        'views/ars_flight_views.xml',
        'views/ars_reservation_views.xml',
        'wizards/ars_reservation_wizard.xml',
        'views/ars_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
