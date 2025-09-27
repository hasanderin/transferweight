# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransferVehicle(models.Model):
    _name = 'transfer.vehicle'
    _description = 'Transfer Vehicle Management'
    _order = 'name'

    name = fields.Char(
        string='Vehicle Name',
        required=True,
        help='Name or identifier of the vehicle'
    )
    
    license_plate = fields.Char(
        string='License Plate',
        required=True,
        help='Vehicle license plate number'
    )
    
    max_capacity = fields.Float(
        string='Maximum Capacity (kg)',
        required=True,
        digits='Product Price',
        help='Maximum weight capacity of the vehicle in kilograms'
    )
    
    current_weight = fields.Float(
        string='Current Weight (kg)',
        digits='Product Price',
        compute='_compute_current_weight',
        store=True,
        help='Current total weight of assigned orders'
    )
    
    capacity_usage_percent = fields.Float(
        string='Capacity Usage (%)',
        digits='Product Price',
        compute='_compute_capacity_usage',
        help='Percentage of capacity currently in use'
    )
    
    state = fields.Selection([
        ('available', 'Available'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('maintenance', 'Maintenance')
    ], string='Status', default='available', required=True)
    
    driver_name = fields.Char(
        string='Driver Name',
        help='Name of the vehicle driver'
    )
    
    driver_phone = fields.Char(
        string='Driver Phone',
        help='Phone number of the vehicle driver'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide the vehicle without deleting it'
    )
    
    # Relations
    sale_order_ids = fields.One2many(
        'sale.order',
        'vehicle_id',
        string='Assigned Orders',
        help='Sales orders assigned to this vehicle'
    )
    
    assigned_order_count = fields.Integer(
        string='Assigned Orders',
        compute='_compute_assigned_order_count',
        help='Number of orders assigned to this vehicle'
    )

    @api.depends('sale_order_ids', 'sale_order_ids.total_weight')
    def _compute_current_weight(self):
        """Calculate current total weight from assigned orders"""
        for vehicle in self:
            total_weight = 0.0
            for order in vehicle.sale_order_ids.filtered(
                lambda o: o.state in ['sale', 'done'] and not o.is_delivered
            ):
                total_weight += order.total_weight or 0.0
            vehicle.current_weight = total_weight

    @api.depends('current_weight', 'max_capacity')
    def _compute_capacity_usage(self):
        """Calculate capacity usage percentage"""
        for vehicle in self:
            if vehicle.max_capacity > 0:
                vehicle.capacity_usage_percent = (vehicle.current_weight / vehicle.max_capacity) * 100
            else:
                vehicle.capacity_usage_percent = 0.0

    @api.depends('sale_order_ids')
    def _compute_assigned_order_count(self):
        """Count assigned orders"""
        for vehicle in self:
            vehicle.assigned_order_count = len(vehicle.sale_order_ids.filtered(
                lambda o: o.state in ['sale', 'done'] and not o.is_delivered
            ))

    @api.constrains('max_capacity')
    def _check_max_capacity(self):
        """Validate maximum capacity is positive"""
        for vehicle in self:
            if vehicle.max_capacity <= 0:
                raise ValidationError(_('Maximum capacity must be greater than 0.'))

    @api.constrains('license_plate')
    def _check_license_plate_unique(self):
        """Ensure license plate is unique"""
        for vehicle in self:
            if vehicle.license_plate:
                existing = self.search([
                    ('license_plate', '=', vehicle.license_plate),
                    ('id', '!=', vehicle.id)
                ])
                if existing:
                    raise ValidationError(_('License plate must be unique.'))

    def action_set_available(self):
        """Set vehicle status to available"""
        self.write({'state': 'available'})

    def action_set_in_transit(self):
        """Set vehicle status to in transit"""
        self.write({'state': 'in_transit'})

    def action_set_completed(self):
        """Set vehicle status to completed"""
        self.write({'state': 'completed'})

    def action_set_maintenance(self):
        """Set vehicle status to maintenance"""
        self.write({'state': 'maintenance'})

    def name_get(self):
        """Custom name display"""
        result = []
        for vehicle in self:
            name = f"{vehicle.name} ({vehicle.license_plate})"
            result.append((vehicle.id, name))
        return result

    @api.model
    def get_available_vehicles(self, required_capacity=0.0):
        """Get available vehicles with sufficient capacity"""
        return self.search([
            ('state', '=', 'available'),
            ('active', '=', True),
            ('max_capacity', '>=', required_capacity)
        ])
