# -*- coding: utf-8 -*-
{
    'name': "Library Book",

    'summary': """
        Best Library Book Ever""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PANG-SORAM-DEPO",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','decimal_precision'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/library_book.xml',
        'views/library_book_categ.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}