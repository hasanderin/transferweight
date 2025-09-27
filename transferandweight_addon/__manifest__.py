# -*- coding: utf-8 -*-
{
    'name': 'Transfer and Weight Management',
    'version': '13.0.1.0.0',
    'category': 'Sales',
    'summary': 'Weight calculation and vehicle management for sales orders',
    'description': """
        Transfer and Weight Management
        =============================
        
        This module provides:
        
        * Weight calculation for sales order lines based on product weight
        * Total weight calculation for sales orders
        * Vehicle management with capacity tracking
        * Vehicle assignment to sales orders
        * Vehicle status tracking (available, in transit, completed)
        * Capacity validation for vehicle assignments
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_views.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
