# -*- coding: utf-8 -*-

{
    'name':"Facturation Ihusi Entreport",
    'description':"""
        Module d'extension vente et facturation pour customization de la facturation chez Ihusi Entrepot
    """,
    'version':'1.0',
    'category': 'Sales/Sales',
    'depends': ['base', 'sale_management'],
    'data':[
        'security/res_groups.xml',
        'views/views.xml',
        # 'reports/account_invoice.xml',
        'reports/sale_report_templates.xml',
        'reports/sale_report.xml'
    ],
    'website':'https://zeslap.com',
    'author':'ZeSlap Platforms',
    'email':'info@zeslap.com',
    'application':False,
    'auto_install':False
}
