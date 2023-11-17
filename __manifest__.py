# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital Management',
    'version': '1.1',
    'summary': 'Hospital Management SoftWare',
    'sequence': 10,
    'description': """Hospital Management SoftWare""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['base', 'product', 'analytic', 'portal', 'digest', 'sale', 'mail', 'website_slides',
                'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'views/patient_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
        'views/partner.xml',
        'views/sale.xml',

        'views/doctor_view.xml',
        'report/patient_details_template.xml',
        'report/patient_card.xml',
        'report/report.xml'

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
