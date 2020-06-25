# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cycle_packaging(models.Model):
    _name = 'cycle.packaging'

    name = fields.Char('Set Secuence', required=True, select=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('reg_code_cycle_packaging'), help="Unique number")
    sale_order = fields.Many2one('sale.order',string="Pedido de venta")
    partner = fields.Many2one('res.partner', related="sale_order.partner_id", store=True, string="Cliente")
    product = fields.Many2one('product.product', string="Producto")
    quantity = fields.Integer(string="Cantidad")
    pending = fields.Integer(string="Pendiente")
    date = fields.Datetime(string="Fecha",default=fields.Datetime.now)
    cycle_packaging_line = fields.One2many('cycle.packaging.line','cycle_packaging',required=True, string="Linea de entrega")
    state = fields.Selection(
        string='Estado',
        selection=[
            ('draft', 'Borrador'), 
            ('open', 'Abierto'), 
            ('done','Hecho'),
            ('incomplete', 'Incompleto')
        ], default="draft"
    )
    merma = fields.Integer(string="Merma")
    reason = fields.Text(string="Motivo de merma")
    invoice = fields.Many2one('account.invoice', string="Factura")


    def action_confirm(self):
        self.state = 'open'
        self.pending = self.quantity

    def action_done(self):
        return {
            'name': "Finalizar Entrega",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'finish.packaging',
            'target': 'new',
            'context': {'current_id': self.id,'default_merma':self.pending, 'partner':self.partner.id,'date':self.date},
        }

    def make_invoice(self):
        self.state = 'done'

    def open_wizard(self):
        return {
            'name': "Entrega",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'delivered.packaging',
            'target': 'new',
            'context': {'current_id': self.id, 'default_delivered': self.pending},
        }

class cycle_packaging(models.Model):
    _name = 'cycle.packaging.line'

    cycle_packaging = fields.Many2one('cycle.packaging')
    delivered = fields.Integer()
    date = fields.Datetime()
    pickinkg = fields.Many2one('stock.picking')

    def delete_line_record(self):
        for line in self:
            if not line.cycle_packaging.state == 'done':
                line.cycle_packaging.pending = line.cycle_packaging.pending + line.delivered
                line.unlink()

class product_cleaning(models.Model):
    _inherit = 'product.template'

    reusable = fields.Boolean(
        string='Es envase reutilizable',
        default=False
    )
    container = fields.Many2one('product.product')
    