# -*- coding: utf-8 -*-

{
    'name':"Ihusi Entreport",
    'description':"""
        Module d'extension vente et facturation pour customization de la facturation chez Ihusi Entrepot
    """,
    'version':'1.0',
    'category': 'Sales/Sales',
    'depends': ['base', 'sale_management','account'],
    'data':[
        'views/views.xml',
        # 'reports/account_invoice.xml',
        'reports/sale_order.xml'
    ],
    'website':'https://zeslap.com',
    'author':'ZeSlap Platforms',
    'email':'info@zeslap.com',
    'application':False
}
