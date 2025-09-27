# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_weight = fields.Float(
        string='Product Weight (kg)',
        related='product_id.weight',
        store=True,
        digits=(16, 2),
        help='Weight of the product per unit'
    )
    
    line_weight = fields.Float(
        string='Line Weight (kg)',
        compute='_compute_line_weight',
        store=True,
        digits=(16, 2),
        help='Total weight for this line (product weight × quantity)'
    )

    @api.depends('product_weight', 'product_uom_qty')
    def _compute_line_weight(self):
        """Calculate line weight based on product weight and quantity"""
        for line in self:
            line.line_weight = (line.product_weight or 0.0) * (line.product_uom_qty or 0.0)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_weight = fields.Float(
        string='Total Weight (kg)',
        compute='_compute_total_weight',
        store=True,
        digits=(16, 2),
        help='Total weight of all order lines'
    )
    
    vehicle_id = fields.Many2one(
        'transfer.vehicle',
        string='Assigned Vehicle',
        tracking=True,
        help='Vehicle assigned to this order'
    )
    
    vehicle_capacity = fields.Float(
        string='Vehicle Capacity (kg)',
        related='vehicle_id.max_capacity',
        digits=(16, 2),
        help='Maximum capacity of the assigned vehicle'
    )
    
    vehicle_current_weight = fields.Float(
        string='Vehicle Current Weight (kg)',
        related='vehicle_id.current_weight',
        digits=(16, 2),
        help='Current weight of the assigned vehicle'
    )
    
    vehicle_capacity_usage = fields.Float(
        string='Vehicle Capacity Usage (%)',
        related='vehicle_id.capacity_usage_percent',
        digits=(5, 2),
        help='Current capacity usage percentage of the assigned vehicle'
    )
    
    vehicle_state = fields.Selection(
        related='vehicle_id.state',
        string='Vehicle Status',
        help='Current status of the assigned vehicle'
    )
    
    is_delivered = fields.Boolean(
        string='Is Delivered',
        default=False,
        help='Mark as delivered to exclude from vehicle weight calculation'
    )
    
    delivery_date = fields.Datetime(
        string='Delivery Date',
        help='Actual delivery date'
    )

    @api.depends('order_line.line_weight')
    def _compute_total_weight(self):
        """Calculate total weight of all order lines"""
        for order in self:
            total_weight = sum(line.line_weight for line in order.order_line)
            order.total_weight = total_weight

    @api.constrains('vehicle_id', 'total_weight')
    def _check_vehicle_capacity(self):
        """Validate vehicle capacity when assigning"""
        for order in self:
            if order.vehicle_id and order.total_weight:
                # Calculate current vehicle weight excluding this order
                other_orders_weight = sum(
                    o.total_weight for o in order.vehicle_id.sale_order_ids
                    if o.id != order.id and o.state in ['sale', 'done'] and not o.is_delivered
                )
                
                total_required_weight = other_orders_weight + order.total_weight
                
                if total_required_weight > order.vehicle_id.max_capacity:
                    raise ValidationError(
                        _('Order weight (%.2f kg) exceeds vehicle capacity. '
                          'Vehicle capacity: %.2f kg, Current usage: %.2f kg') %
                        (order.total_weight, order.vehicle_id.max_capacity, other_orders_weight)
                    )

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        """Update vehicle information when vehicle is changed"""
        if self.vehicle_id:
            # Check if vehicle is available
            if self.vehicle_id.state != 'available':
                return {
                    'warning': {
                        'title': _('Vehicle Not Available'),
                        'message': _('Selected vehicle is not available. Status: %s') %
                                 dict(self.vehicle_id._fields['state'].selection)[self.vehicle_id.state]
                    }
                }

    def action_assign_vehicle(self):
        """Action to assign a vehicle to the order"""
        self.ensure_one()
        
        if not self.total_weight:
            raise ValidationError(_('Cannot assign vehicle: Order has no weight calculated.'))
        
        if self.state not in ['sale', 'done']:
            raise ValidationError(_('Can only assign vehicle to confirmed orders.'))
        
        # Find available vehicles with sufficient capacity
        available_vehicles = self.env['transfer.vehicle'].get_available_vehicles(self.total_weight)
        
        if not available_vehicles:
            raise ValidationError(
                _('No available vehicles found with sufficient capacity for %.2f kg.') %
                self.total_weight
            )
        
        # If only one vehicle available, assign it automatically
        if len(available_vehicles) == 1:
            self.vehicle_id = available_vehicles[0]
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Vehicle Assigned'),
                    'message': _('Vehicle %s has been assigned to this order.') % available_vehicles[0].name,
                    'type': 'success',
                }
            }
        
        # Multiple vehicles available - show wizard or let user choose
        return {
            'name': _('Assign Vehicle'),
            'type': 'ir.actions.act_window',
            'res_model': 'transfer.vehicle',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', available_vehicles.ids)],
            'context': {
                'default_sale_order_id': self.id,
                'select_vehicle': True,
            },
            'target': 'new',
        }

    def action_mark_delivered(self):
        """Mark order as delivered"""
        self.ensure_one()
        if not self.vehicle_id:
            raise ValidationError(_('Cannot mark as delivered: No vehicle assigned.'))
        
        self.write({
            'is_delivered': True,
            'delivery_date': fields.Datetime.now(),
        })
        
        # Update vehicle status if all orders are delivered
        if all(order.is_delivered for order in self.vehicle_id.sale_order_ids.filtered(
            lambda o: o.state in ['sale', 'done']
        )):
            self.vehicle_id.action_set_completed()

    def action_unassign_vehicle(self):
        """Remove vehicle assignment from order"""
        self.ensure_one()
        if self.vehicle_id:
            vehicle_name = self.vehicle_id.name
            self.vehicle_id = False
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Vehicle Unassigned'),
                    'message': _('Vehicle %s has been unassigned from this order.') % vehicle_name,
                    'type': 'info',
                }
            }

    @api.model
    def get_orders_by_vehicle(self, vehicle_id):
        """Get all orders assigned to a specific vehicle"""
        return self.search([
            ('vehicle_id', '=', vehicle_id),
            ('state', 'in', ['sale', 'done'])
        ])
