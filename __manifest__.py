# -*- coding: utf-8 -*-
{
    'name': "Transferencia de Cheques",

    'summary': """
        Módulo para la transferencia de cheques entre bancos.
        """,

    'description': """
        Módulo para la transferencia de cheques entre bancos. Permite registrar la transferencia de cheques emitidos y recibidos entre diferentes cuentas bancarias dentro de la misma empresa.
    """,

    'author': "GonzaOdoo",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    "data": ["security/ir.model.access.csv",
             "views/check_views.xml",
            ],
}
