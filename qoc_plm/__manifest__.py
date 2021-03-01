# -*- coding: utf-8 -*-
{
    'name': "QOC - PLM Revision Management",

    'summary': """
        Version Control Management""",

    'description': """
        Take control of your version management! This app will create a new product variant
        for each revision of a product you make. This way you can sell and produce both old
        and new versions for each of your prouducts. Want to depricate and old version? All you 
        have to do is remove the variant! All product information will be archived and no longer
        available to sell. It's that easy!
    """,

    'author': "QOC Innovations",
    'website': "http://www.qocinnovations.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mrp_plm','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
