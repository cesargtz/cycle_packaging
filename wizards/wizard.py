# -*- coding: utf-8 -*-

from odoo import models, fields, api

class createDeliveredPackaging(models.TransientModel):
    _name = 'delivered.packaging'
 
    delivered = fields.Integer(string="Entregado")
    date = fields.Datetime(string="Fecha",default=fields.Datetime.now)

    def action_delivered(self):
        context = self.env.context
        move = self.env['cycle.packaging'].search([('id','=',context.get('current_id'))])
        pending = move['pending']
        move.write({'pending':(pending - self.delivered)})
        packaging_line = self.env['cycle.packaging.line'].create({
            'cycle_packaging': context.get('current_id'),
            'delivered': self.delivered,
            'date' : self.date,
        })
        picking = self.env['stock.picking'].create({
            'partner_id': move.sale_order.partner_id.id,
            'picking_type_id': 1,
            'scheduled_date': move.date,
            'origin': move.name,
            'location_id':4,
            'location_dest_id':8,
        })
        self.env['stock.move'].create({
            'name':'test',
            'picking_id': picking.id,
            'product_id': move.product.id,
            'product_uom_qty': self.delivered,
            'quantity_done': self.delivered,
            'product_uom': 1,
            'location_id':4,
            'location_dest_id':8,
        })
        picking._compute_show_operations()
        picking.action_confirm()
        picking.action_assign()
        picking._autoconfirm_picking()
        picking.button_validate()
        picking.action_done()
        packaging_line.write({'pickinkg':picking})
        if self.delivered >= pending:
            move.write({'state':'done'})

class FinishCyclePackaging(models.TransientModel):
    _name = 'finish.packaging'
 
    merma = fields.Integer(string="Merma")
    motivo = fields.Text(
        string='Motivo',
    )
    make_invoice = fields.Boolean(
        default=False
    )

    def action_finish(self):
        context = self.env.context
        move = self.env['cycle.packaging'].search([('id','=',context.get('current_id'))])
        move.write({'merma':self.merma})
        if not self.make_invoice:
            move.write({'state':'incomplete'})
            move.write({'reason':self.motivo})
        # else:
        #     # Make invoice, incomplete to define accounts and journals
        #     invoice_id = self.env['account.move'].create({
        #         'partner_id' : context.get('partner'),
        #         'type':'out_invoice',
        #         'date_invoice':context.get('date'),
        #         'state':'draft',
		# 	})
        #     move_id = self.env['account.move.line'].create({
		# 			'move_id': invoice_id.id,
		# 			'quantity' :self.merma,
		# 			'name': 'Merma Envases',
		# 		})
        #     move.write({'invoice':invoice_id})
    