# -*- coding: utf-8 -*-
{
    'name': 'Transfer and Weight Management',
    'version': '13.0.1.0.0',
    'category': 'Sales',
    'summary': 'Weight calculation and vehicle management for sales orders',
    'description': """
        Transfer and Weight Management Module
        
        This module provides weight calculation for sales order lines based on product weight,
        total weight calculation for sales orders, vehicle management with capacity tracking,
        vehicle assignment to sales orders, vehicle status tracking (available, in transit, completed),
        and capacity validation for vehicle assignments.
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
