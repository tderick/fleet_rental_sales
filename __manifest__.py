# -*- coding: utf-8 -*-
{
    'name': "fleet_rental_sales",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "DERICK TEMFACK",
    'website': "https://github.com/tderick/fleet_rental_sales",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'sale_management', 'stock', 'account'],

    # always loaded
    'data': [
        'views/fleet_vehicle_view_form.xml',
        'views/account_move_form.xml',
        'views/car_contract_result_form.xml',
        'views/fleet_vehicle_log_contract_form.xml',

    ]
}
